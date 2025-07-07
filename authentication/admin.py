from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_superuser', 'created_at', 'last_login', 'profile_image_display')
    list_filter  = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
        (None,               {'fields': ('email', 'password')}),
        ('Personal Info',    {'fields': ('full_name', 'profile_image')}),
        ('Permissions',      {'fields': ('role', 'is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates',  {'fields': ('last_login','created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name','password1','password2','role','is_active','is_staff','profile_image'),
        }),
    )

    readonly_fields = ('created_at', 'last_login')

    def profile_image_display(self, obj):
        if obj.profile_image:
            return f"<img src='{obj.profile_image.url}' width='40' height='40' style='object-fit:cover;border-radius:50%;' />"
        return "-"
    profile_image_display.short_description = 'Profile Image'
    profile_image_display.allow_tags = True
