from django.test import TestCase
from .models import Hospital, HospitalBranch, Doctor

class HospitalModelTests(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name='Test Hospital',
            email='hospital@example.com',
            address='123 Main St',
            phone='1234567890',
            website='http://testhospital.com',
            is_verified=True
        )
        self.branch = HospitalBranch.objects.create(
            hospital=self.hospital,
            name='Main Branch',
            address='123 Main St',
            phone='1234567890',
            city='Test City',
            state='Test State',
            manager='Manager Name'
        )
        self.doctor = Doctor.objects.create(
            branch=self.branch,
            name='Dr. John Doe',
            specialization='Cardiology',
            available_times='["Mon 9-11am"]',
            contact_info='doctor@example.com'
        )

    def test_hospital_creation(self):
        self.assertEqual(Hospital.objects.count(), 1)
        self.assertEqual(self.hospital.name, 'Test Hospital')
        self.assertTrue(self.hospital.is_verified)

    def test_branch_uniqueness(self):
        with self.assertRaises(Exception):
            HospitalBranch.objects.create(
                hospital=self.hospital,
                name='Main Branch',
                address='Another Address',
                phone='0987654321',
                city='Another City',
                state='Another State'
            )

    def test_doctor_creation_and_relationship(self):
        self.assertEqual(self.branch.doctors.count(), 1)
        self.assertEqual(self.doctor.branch, self.branch)
        self.assertEqual(self.doctor.specialization, 'Cardiology')
