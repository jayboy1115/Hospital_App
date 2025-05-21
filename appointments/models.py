from django.db import models
from patients.models import Patient
from hospitals.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient          = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor           = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.DateTimeField()
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'appointment_time')  

    def __str__(self):
        return f"{self.patient.universal_id} ➔ Dr.{self.doctor.name} @ {self.appointment_time}"
