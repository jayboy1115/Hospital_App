from django.test import TestCase
from .models import Patient
from authentication.models import User
from hospitals.models import Hospital, HospitalBranch
from datetime import date

class PatientModelTests(TestCase):
    def setUp(self):
        import uuid
        unique_email = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        self.user = User.objects.create_user(email=unique_email, password='testpass123', full_name='Patient User')
        self.hospital = Hospital.objects.create(name='Test Hospital', email=f"hospital_{uuid.uuid4()}@example.com", address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name=f'Main Branch {uuid.uuid4().hex[:4]}', address='123 St', phone='1234567890', city='City', state='State')
        self.patient = Patient.objects.create(
            user=self.user,
            hospital_branch=self.branch,
            universal_id=unique_universal_id,
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='1234567890',
            address='123 Street',
            emergency_contact='Emergency Contact',
            medical_history='None'
        )

    def test_patient_creation(self):
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(self.patient.user.email, 'patient@example.com')
        self.assertEqual(self.patient.universal_id, 'P123')
        self.assertEqual(self.patient.gender, 'M')
        self.assertEqual(self.patient.hospital_branch, self.branch)

    def test_universal_id_uniqueness(self):
        import uuid
        with self.assertRaises(Exception):
            Patient.objects.create(
                user=User.objects.create_user(email=f"other_{uuid.uuid4()}@example.com", password='testpass123', full_name='Other User'),
                hospital_branch=self.branch,
                universal_id=self.patient.universal_id
            )

    def test_update_patient_profile(self):
        self.patient.address = 'New Address'
        self.patient.emergency_contact = 'New Contact'
        self.patient.save()
        updated = Patient.objects.get(id=self.patient.id)
        self.assertEqual(updated.address, 'New Address')
        self.assertEqual(updated.emergency_contact, 'New Contact')

    def test_delete_patient_cascades(self):
        user_id = self.user.id
        self.patient.delete()
        self.assertFalse(Patient.objects.filter(id=self.patient.id).exists())
        self.assertTrue(User.objects.filter(id=user_id).exists())  # User remains, only patient deleted

    def test_patient_str_and_optional_fields(self):
        import uuid
        patient_str = str(self.patient)
        self.assertIn(self.patient.universal_id, patient_str)
        # Test with missing optional fields
        patient2 = Patient.objects.create(
            user=User.objects.create_user(email=f"opt_{uuid.uuid4()}@example.com", password='testpass123', full_name='Opt User'),
            universal_id=f"P{uuid.uuid4().hex[:8]}"
        )
        self.assertEqual(patient2.address, '')
