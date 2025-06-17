# chatbot/admin.py
from django.contrib import admin
from .models import ChatbotSession

@admin.register(ChatbotSession)
class ChatbotSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'symptoms', 'created_at')
    search_fields = ('symptoms', 'patient__universal_id')
    list_filter = ('created_at',)
