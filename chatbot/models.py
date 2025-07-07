
from django.db import models
from patients.models import Patient

class ChatbotSession(models.Model):
    patient          = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chat_sessions')
    symptoms         = models.TextField()
    suggested_drugs  = models.JSONField(blank=True, null=True, default=list, help_text="List of suggested drugs")
    recommendation   = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} for {self.patient.universal_id}"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatbotSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=[('PATIENT', 'Patient'), ('BOT', 'Bot')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}: {self.message[:30]}..."
