# eventapp/admin.py

from django.contrib import admin
from .models import CustomUser, UserProfile

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    # Add fields you want to display in the admin interface

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    # Add fields you want to display in the admin interface

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
