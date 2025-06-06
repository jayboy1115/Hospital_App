from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_superuser')
    list_filter  = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
        (None,               {'fields': ('email', 'password')}),
        ('Personal Info',    {'fields': ('full_name',)}),
        ('Permissions',      {'fields': ('role', 'is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates',  {'fields': ('last_login','created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name','password1','password2','role','is_active','is_staff'),
        }),
    )
