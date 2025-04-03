from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings

from app.models import User, UserLoginHistory

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> User:
        return authenticate(username=username, password=password)

    @staticmethod
    def login_user(request, user: User) -> None:
        UserLoginHistory.objects.create(user=user, ip=request.META.get('REMOTE_ADDR'))
        auth_login(request, user)

    @staticmethod
    def logout_user(request) -> None:
        auth_login(request, None)

    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email address.")

        # Unique username and email check
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")

        # Hash password
        salt = settings.PASSWORD_SALT
        hashed_password = make_password(password, salt=salt, hasher='pbkdf2_sha256')
        
        return User.objects.create(
            username=username,
            email=email,
            password=hashed_password
        ) 