from django.test import TestCase
from .models import Patient
from authentication.models import User
from hospitals.models import Hospital, HospitalBranch
from datetime import date

class PatientModelTests(TestCase):
    def setUp(self):
        import uuid
        # Clean up all users and patients before each test
        Patient.objects.all().delete()
        User.objects.all().delete()
        self.hospital = Hospital.objects.create(name=f'Test Hospital {uuid.uuid4().hex[:8]}', email=f"hospital_{uuid.uuid4()}@example.com", address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name=f'Main Branch {uuid.uuid4().hex[:8]}', address='123 St', phone='1234567890', city='City', state='State')

    def _create_unique_user(self, prefix='patient'):
        import uuid
        unique_email = f"{prefix}_{uuid.uuid4()}@example.com"
        user = User.objects.create_user(email=unique_email, password='testpass123', full_name=f'{prefix.capitalize()} User')
        # Patient is auto-created by signal
        return user

    def test_patient_creation(self):
        import uuid
        user = self._create_unique_user()
        # Get the auto-created patient
        patient = Patient.objects.get(user=user)
        # Update fields as needed
        patient.hospital_branch = self.branch
        patient.date_of_birth = date(2000, 1, 1)
        patient.gender = 'M'
        patient.phone = '1234567890'
        patient.address = '123 Street'
        patient.emergency_contact = 'Emergency Contact'
        patient.medical_history = 'None'
        patient.save()
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(patient.user.email, user.email)
        self.assertEqual(patient.gender, 'M')
        self.assertEqual(patient.hospital_branch, self.branch)

    def test_universal_id_uniqueness(self):
        import uuid
        user1 = self._create_unique_user()
        patient = Patient.objects.get(user=user1)
        patient.hospital_branch = self.branch
        patient.date_of_birth = date(2000, 1, 1)
        patient.gender = 'M'
        patient.phone = '1234567890'
        patient.address = '123 Street'
        patient.emergency_contact = 'Emergency Contact'
        patient.medical_history = 'None'
        patient.save()
        # Create a new unique user, but reuse the same universal_id (should fail)
        new_user = self._create_unique_user('other')
        with self.assertRaises(Exception):
            Patient.objects.create(
                user=new_user,
                hospital_branch=self.branch,
                universal_id=patient.universal_id
            )

    def test_update_patient_profile(self):
        user = self._create_unique_user()
        patient = Patient.objects.get(user=user)
        patient.hospital_branch = self.branch
        patient.date_of_birth = date(2000, 1, 1)
        patient.gender = 'M'
        patient.phone = '1234567890'
        patient.address = '123 Street'
        patient.emergency_contact = 'Emergency Contact'
        patient.medical_history = 'None'
        patient.save()
        patient.address = 'New Address'
        patient.emergency_contact = 'New Contact'
        patient.save()
        updated = Patient.objects.get(id=patient.id)
        self.assertEqual(updated.address, 'New Address')
        self.assertEqual(updated.emergency_contact, 'New Contact')

    def test_delete_patient_cascades(self):
        user = self._create_unique_user()
        patient = Patient.objects.get(user=user)
        patient.hospital_branch = self.branch
        patient.date_of_birth = date(2000, 1, 1)
        patient.gender = 'M'
        patient.phone = '1234567890'
        patient.address = '123 Street'
        patient.emergency_contact = 'Emergency Contact'
        patient.medical_history = 'None'
        patient.save()
        user_id = user.id
        patient.delete()
        self.assertFalse(Patient.objects.filter(id=patient.id).exists())
        self.assertTrue(User.objects.filter(id=user_id).exists())  # User remains, only patient deleted

    def test_patient_str_and_optional_fields(self):
        user = self._create_unique_user()
        patient = Patient.objects.get(user=user)
        patient.hospital_branch = self.branch
        patient.date_of_birth = date(2000, 1, 1)
        patient.gender = 'M'
        patient.phone = '1234567890'
        patient.address = '123 Street'
        patient.emergency_contact = 'Emergency Contact'
        patient.medical_history = 'None'
        patient.save()
        patient_str = str(patient)
        self.assertIn(patient.universal_id, patient_str)
        # Test with missing optional fields, using a unique user and universal_id
        opt_user = self._create_unique_user('opt')
        patient2 = Patient.objects.get(user=opt_user)
        patient2.hospital_branch = self.branch
        patient2.save()
        self.assertEqual(patient2.address, '')
