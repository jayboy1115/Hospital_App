from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Appointment
from hospitals.models import Hospital, HospitalBranch, Doctor
from patients.models import Patient
from authentication.models import User
from django.utils import timezone
from datetime import timedelta


class AppointmentTests(APITestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name='Test Hospital', email='hospital@example.com', address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name='Main Branch', address='123 St', phone='1234567890', city='City', state='State')
        self.doctor = Doctor.objects.create(branch=self.branch, name='Dr. Who', specialization='General', available_times='["Mon 9-11am"]')
        self.user = User.objects.create_user(email='patient@example.com', password='testpass123', full_name='Patient User')
        self.patient = Patient.objects.create(user=self.user, hospital_branch=self.branch, universal_id='P123')
        self.client.force_authenticate(user=self.user)

    def test_create_appointment(self):
        url = reverse('appointment-list') if 'appointment-list' in [u.name for u in self.client.handler._urls.urlpatterns] else '/appointments/'
        data = {
            'doctor': self.doctor.id,
            'appointment_time': (timezone.now() + timedelta(days=1)).isoformat(),
            'reason': 'Routine checkup',
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertTrue(Appointment.objects.filter(doctor=self.doctor).exists())

    def test_double_booking(self):
        appointment_time = timezone.now() + timedelta(days=1)
        Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_time=appointment_time)
        url = reverse('appointment-list') if 'appointment-list' in [u.name for u in self.client.handler._urls.urlpatterns] else '/appointments/'
        data = {
            'doctor': self.doctor.id,
            'appointment_time': appointment_time.isoformat(),
            'reason': 'Routine checkup',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This slot is already booked.', str(response.data))

    def test_past_appointment_time(self):
        url = reverse('appointment-list') if 'appointment-list' in [u.name for u in self.client.handler._urls.urlpatterns] else '/appointments/'
        data = {
            'doctor': self.doctor.id,
            'appointment_time': (timezone.now() - timedelta(days=1)).isoformat(),
            'reason': 'Past appointment',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Appointment time must be in the future.', str(response.data))
