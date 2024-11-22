from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'birthdate')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', 'birthdate')}),
    )