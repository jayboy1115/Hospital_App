import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Patient
from authentication.models import User


def generate_universal_id():
    """Returns an 8-character uppercase alphanumeric ID."""
    return uuid.uuid4().hex[:8].upper()


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    When a User is created with role PATIENT, auto-create a Patient record.
    """
    if created and instance.role == 'PATIENT':
        Patient.objects.create(
            user=instance,
            universal_id=generate_universal_id()
        )