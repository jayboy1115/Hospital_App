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

    def test_update_hospital_and_branch(self):
        self.hospital.name = 'Updated Hospital'
        self.hospital.save()
        self.branch.city = 'Updated City'
        self.branch.save()
        self.assertEqual(Hospital.objects.get(id=self.hospital.id).name, 'Updated Hospital')
        self.assertEqual(HospitalBranch.objects.get(id=self.branch.id).city, 'Updated City')

    def test_delete_hospital_cascades(self):
        hospital_id = self.hospital.id
        self.hospital.delete()
        self.assertFalse(Hospital.objects.filter(id=hospital_id).exists())
        self.assertEqual(HospitalBranch.objects.filter(hospital_id=hospital_id).count(), 0)
        self.assertEqual(Doctor.objects.filter(branch__hospital_id=hospital_id).count(), 0)

    def test_doctor_available_times_format(self):
        import json
        times = json.loads(self.doctor.available_times)
        self.assertIsInstance(times, list)
        self.assertIn('Mon 9-11am', times)

    def test_filter_doctors_by_specialization(self):
        Doctor.objects.create(branch=self.branch, name='Dr. Jane', specialization='Pediatrics', available_times='["Tue 10-12am"]')
        cardiologists = Doctor.objects.filter(specialization='Cardiology')
        self.assertIn(self.doctor, cardiologists)
