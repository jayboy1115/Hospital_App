from django.test import TestCase
from .models import Patient
from authentication.models import User
from hospitals.models import Hospital, HospitalBranch
from datetime import date

class PatientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='patient@example.com', password='testpass123', full_name='Patient User')
        self.hospital = Hospital.objects.create(name='Test Hospital', email='hospital@example.com', address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name='Main Branch', address='123 St', phone='1234567890', city='City', state='State')
        self.patient = Patient.objects.create(
            user=self.user,
            hospital_branch=self.branch,
            universal_id='P123',
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
        with self.assertRaises(Exception):
            Patient.objects.create(
                user=User.objects.create_user(email='other@example.com', password='testpass123', full_name='Other User'),
                hospital_branch=self.branch,
                universal_id='P123'
            )
