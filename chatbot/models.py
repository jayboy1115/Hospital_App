from django.db import models
from patients.models import Patient

class ChatbotSession(models.Model):
    patient          = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chat_sessions')
    symptoms         = models.TextField()
    suggested_drugs  = models.TextField(blank=True)
    recommendation   = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} for {self.patient.universal_id}"
