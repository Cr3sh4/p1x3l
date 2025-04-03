from django.contrib import admin

# Register your models here.

from app.models import User, UserLoginHistory

admin.site.register(User)
admin.site.register(UserLoginHistory)

