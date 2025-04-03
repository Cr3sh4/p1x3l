import mimetypes

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from app.models import User, StoredFile
from app.services.auth_service import AuthService
from app.services.file_service import FileService

def index(request):
    public_images = FileService.get_public_files()
    return render(request, "index.html", {"public_images": public_images})

def get_auth_state(request):
    if request.user.is_authenticated:
        return HttpResponse("Authenticated, username: " + request.user.username)
    return HttpResponse("Not authenticated.")

def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in.")
            return redirect("index")
        return render(request, 'login.html')
    
    if request.method == "POST":
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in.")
            return redirect("index")

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "All fields are required.")
            return redirect("login")

        user = AuthService.authenticate_user(username, password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

        AuthService.login_user(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect("index")

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in.")
            return redirect("index")
        return render(request, 'register.html')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in.")
            return redirect("index")

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        try:
            user = AuthService.register_user(username, email, password)
            AuthService.login_user(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("index")
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("register")

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")

@login_required
def upload_file(request):
    """Handle file uploads."""
    if request.method == "POST":
        try:
            uploaded_file = request.FILES.get("file")
            is_public = request.POST.get("is_public") == "true"
            
            stored_file = FileService.create_stored_file(
                user=request.user,
                uploaded_file=uploaded_file,
                is_public=is_public
            )
            return JsonResponse({"message": "File uploaded", "file_id": stored_file.id})
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)

    return render(request, "upload.html")

def serve_public_file(request, unique_key):
    try:
        stored_file = get_object_or_404(StoredFile, public_link=f"/public/{unique_key}/")
        FileService.check_file_permission(stored_file, request.user)
        FileService.increment_file_views(stored_file)

        file_mime_type, _ = mimetypes.guess_type(stored_file.file.name)
        response = FileResponse(stored_file.file.open(), content_type=file_mime_type)
        response["Content-Disposition"] = f'inline; filename="{stored_file.file.name}"'
        return response
    except PermissionDenied:
        messages.error(request, "You do not have permission to access this file.")
        return redirect("index")
    except Exception as e:
        messages.error(request, "An error occurred while serving the file.")
        return redirect("index")

@login_required
def delete_file(request, file_id):
    try:
        stored_file = get_object_or_404(StoredFile, id=file_id)
        FileService.delete_file(stored_file, request.user)
        return JsonResponse({"success": True})
    except PermissionDenied:
        return JsonResponse({"error": "You do not have permission to delete this file."}, status=403)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

@login_required
def toggle_file_visibility(request, file_id):
    try:
        file = get_object_or_404(StoredFile, id=file_id)
        is_public = FileService.toggle_file_visibility(file, request.user)
        return JsonResponse({
            "success": True,
            "is_public": is_public,
            "file_id": file.id
        })
    except PermissionDenied:
        return JsonResponse({"error": "You do not have permission to modify this file."}, status=403)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

@login_required
def user_profile(request, userid):
    user = get_object_or_404(User, id=userid)
    stored_files = FileService.get_user_files(user, public_only=True)
    
    response = {
        "user": user,
        "stored_files": stored_files
    }
    return render(request, "user_profile.html", {"user_data": response})

@login_required
def my_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect("index")

    stored_files = FileService.get_user_files(request.user)
    response = {
        "user": request.user,
        "stored_files": stored_files
    }
    return render(request, "profile/profile.html", {"user_data": response})
