import mimetypes
from django.core.exceptions import ValidationError, PermissionDenied
from app.models import StoredFile, User

class FileService:
    ALLOWED_MIME_TYPES = [
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
        "image/svg+xml"
    ]
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    @staticmethod
    def validate_file(uploaded_file) -> None:
        if not uploaded_file:
            raise ValidationError("No file uploaded")

        file_mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        if file_mime_type not in FileService.ALLOWED_MIME_TYPES:
            raise ValidationError("File type not allowed")

        if uploaded_file.size > FileService.MAX_FILE_SIZE:
            raise ValidationError("File size limit exceeded")

    @staticmethod
    def check_file_permission(file: StoredFile, user: User) -> None:
        if not file.is_public and file.user != user:
            raise PermissionDenied("You do not have permission to access this file.")

    @staticmethod
    def create_stored_file(user: User, uploaded_file, is_public: bool) -> StoredFile:
        FileService.validate_file(uploaded_file)
        
        return StoredFile.objects.create(
            user=user,
            file=uploaded_file,
            is_public=is_public
        )

    @staticmethod
    def get_user_files(user: User, public_only: bool = False):
        query = StoredFile.objects.filter(user=user)
        if public_only:
            query = query.filter(is_public=True)
        return query.order_by("-created_at")

    @staticmethod
    def get_public_files():
        return StoredFile.objects.filter(is_public=True).order_by("-created_at")

    @staticmethod
    def toggle_file_visibility(file: StoredFile, user: User) -> bool:
        if file.user != user:
            raise PermissionDenied("You do not have permission to modify this file.")
            
        file.is_public = not file.is_public
        file.save()
        return file.is_public

    @staticmethod
    def increment_file_views(file: StoredFile) -> None:
        file.views += 1
        file.save()

    @staticmethod
    def delete_file(file: StoredFile, user: User) -> None:
        if file.user != user:
            raise PermissionDenied("You do not have permission to delete this file.")
        file.delete() 