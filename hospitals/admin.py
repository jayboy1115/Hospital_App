from django.contrib import admin
from .models import Hospital, HospitalBranch, Doctor

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)

@admin.register(HospitalBranch)
class HospitalBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital', 'city', 'state', 'created_at')
    search_fields = ('name', 'hospital__name', 'city', 'state')
    readonly_fields = ('created_at',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'branch', 'created_at')
    search_fields = ('name', 'specialization', 'branch__name')
    readonly_fields = ('created_at',)
