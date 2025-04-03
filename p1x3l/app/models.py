import mimetypes
import os
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from p1x3l import settings

class User(AbstractUser):
    rank = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # Override save and hash password
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            # salt = os.getenv("PASSWORD_SALT")
            salt = settings.PASSWORD_SALT
            self.password = make_password(self.password, salt=salt, hasher='pbkdf2_sha256')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class UserLoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.ip

def file_upload_path(instance, filename):
    """Generate a unique file path per user."""
    return f"user_content/user_{instance.user.id}/{uuid.uuid4().hex}_{filename}"


class StoredFile(models.Model):
    """Model to store user-uploaded images."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=file_upload_path)
    file_bytes = models.PositiveIntegerField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    public_link = models.CharField(max_length=255, unique=True)

    def generate_public_link(self):
        """Generate a unique public link if file is public."""
        return f"/public/{slugify(self.user.username)}-{uuid.uuid4().hex[:8]}/"

    def save(self, *args, **kwargs):
        """Override save method to store file size and create a public link if needed."""
        if self.file and not self.file_bytes:
            self.file_bytes = self.file.size

        self.public_link = self.generate_public_link()

        super().save(*args, **kwargs)

    def is_image(self):
        """Check if file is an image based on MIME type."""
        file_mime_type, _ = mimetypes.guess_type(self.file.name)
        return file_mime_type and file_mime_type.startswith("image")

    def __str__(self):
        return f"{self.user.username} - {os.path.basename(self.file.name)}"


