from django.db import models
from authentication.models import User
from hospitals.models import HospitalBranch

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital_branch = models.ForeignKey(HospitalBranch, on_delete=models.SET_NULL, null=True, blank=True)
    universal_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.universal_id})"

