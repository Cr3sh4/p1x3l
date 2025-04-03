from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    # Authentication
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("auth_state/", views.get_auth_state, name="auth_state"),
    path("logout/", views.logout_user, name="logout"),
    # File management
    path("upload/", views.upload_file, name="upload_file"),
    path("public/<str:unique_key>/", views.serve_public_file, name="serve_public_file"),
    path("toggle_file_visibility/<int:file_id>/", views.toggle_file_visibility, name="toggle_file_visibility"),
    path("delete_file/<int:file_id>/", views.delete_file, name="delete_file"),
    # User profile
    path("user/<int:userid>/", views.user_profile, name="user_profile"),
    path("profile/", views.my_profile, name="my_profile"),
    path("admin/", admin.site.urls),
]
