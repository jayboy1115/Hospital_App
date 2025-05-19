

from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HospitalBranch(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='branches')
    name     = models.CharField(max_length=255)
    address  = models.TextField()
    phone    = models.CharField(max_length=20)
    city     = models.CharField(max_length=100)
    state    = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.hospital.name}"


class Doctor(models.Model):
    branch         = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='doctors')
    name           = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    available_times = models.TextField(
        help_text="JSON or comma-separated slots, e.g. '[\"Mon 9-11am\",\"Tue 2-4pm\"]'"
    )
    contact_info   = models.CharField(max_length=255, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
