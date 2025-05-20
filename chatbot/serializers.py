from rest_framework import serializers
from .models import ChatbotSession

class ChatbotSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotSession
        fields = ['id', 'symptoms', 'suggested_drugs', 'recommendation', 'created_at']
        read_only_fields = ['id', 'suggested_drugs', 'recommendation', 'created_at']
