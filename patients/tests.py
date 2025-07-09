from django.test import TransactionTestCase
from .models import Patient
from authentication.models import User
from hospitals.models import Hospital, HospitalBranch
from datetime import date

class PatientModelTests(TransactionTestCase):
    def setUp(self):
        import uuid
        from django.db import connection
        # Reset user PK sequence for PostgreSQL to avoid unique constraint errors
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE authentication_user_id_seq RESTART WITH 1000;")
        self.hospital = Hospital.objects.create(name=f'Test Hospital {uuid.uuid4().hex[:4]}', email=f"hospital_{uuid.uuid4()}@example.com", address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name=f'Main Branch {uuid.uuid4().hex[:4]}', address='123 St', phone='1234567890', city='City', state='State')

    def test_patient_creation(self):
        import uuid
        unique_email = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(email=unique_email, password='testpass123', full_name='Patient User')
        patient = Patient.objects.create(
            user=user,
            hospital_branch=self.branch,
            universal_id=unique_universal_id,
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='1234567890',
            address='123 Street',
            emergency_contact='Emergency Contact',
            medical_history='None'
        )
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(patient.user.email, unique_email)
        self.assertEqual(patient.universal_id, unique_universal_id)
        self.assertEqual(patient.gender, 'M')
        self.assertEqual(patient.hospital_branch, self.branch)

    def test_universal_id_uniqueness(self):
        import uuid
        unique_email1 = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        user1 = User.objects.create_user(email=unique_email1, password='testpass123', full_name='Patient User')
        patient = Patient.objects.create(
            user=user1,
            hospital_branch=self.branch,
            universal_id=unique_universal_id,
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='1234567890',
            address='123 Street',
            emergency_contact='Emergency Contact',
            medical_history='None'
        )
        # Create a new unique user, but reuse the same universal_id (should fail)
        unique_email2 = f"other_{uuid.uuid4()}@example.com"
        new_user = User.objects.create_user(email=unique_email2, password='testpass123', full_name='Other User')
        with self.assertRaises(Exception):
            Patient.objects.create(
                user=new_user,
                hospital_branch=self.branch,
                universal_id=patient.universal_id
            )

    def test_update_patient_profile(self):
        import uuid
        unique_email = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(email=unique_email, password='testpass123', full_name='Patient User')
        patient = Patient.objects.create(
            user=user,
            hospital_branch=self.branch,
            universal_id=unique_universal_id,
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='1234567890',
            address='123 Street',
            emergency_contact='Emergency Contact',
            medical_history='None'
        )
        patient.address = 'New Address'
        patient.emergency_contact = 'New Contact'
        patient.save()
        updated = Patient.objects.get(id=patient.id)
        self.assertEqual(updated.address, 'New Address')
        self.assertEqual(updated.emergency_contact, 'New Contact')

    def test_delete_patient_cascades(self):
        import uuid
        unique_email = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(email=unique_email, password='testpass123', full_name='Patient User')
        patient = Patient.objects.create(
            user=user,
            hospital_branch=self.branch,
            universal_id=unique_universal_id,
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='1234567890',
            address='123 Street',
            emergency_contact='Emergency Contact',
            medical_history='None'
        )
        user_id = user.id
        patient.delete()
        self.assertFalse(Patient.objects.filter(id=patient.id).exists())
        self.assertTrue(User.objects.filter(id=user_id).exists())  # User remains, only patient deleted

    def test_patient_str_and_optional_fields(self):
        import uuid
        unique_email = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(email=unique_email, password='testpass123', full_name='Patient User')
        patient = Patient.objects.create(
            user=user,
            hospital_branch=self.branch,
            universal_id=unique_universal_id,
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='1234567890',
            address='123 Street',
            emergency_contact='Emergency Contact',
            medical_history='None'
        )
        patient_str = str(patient)
        self.assertIn(patient.universal_id, patient_str)
        # Test with missing optional fields, using a unique user and universal_id
        opt_email = f"opt_{uuid.uuid4()}@example.com"
        opt_universal_id = f"P{uuid.uuid4().hex[:8]}"
        patient2 = Patient.objects.create(
            user=User.objects.create_user(email=opt_email, password='testpass123', full_name='Opt User'),
            hospital_branch=self.branch,
            universal_id=opt_universal_id
        )
        self.assertEqual(patient2.address, '')
