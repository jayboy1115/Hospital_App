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
        # Use the auto-created Patient from the signal and update its fields
        self.patient = Patient.objects.get(user=self.user)
        self.patient.hospital_branch = self.branch
        self.patient.universal_id = 'P123'
        self.patient.save()
        self.client.force_authenticate(user=self.user)

    def test_create_appointment(self):
        try:
            url = reverse('appointment-list')
        except Exception:
            url = '/api/appointments/my/'
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
        try:
            url = reverse('appointment-list')
        except Exception:
            url = '/api/appointments/my/'
        data = {
            'doctor': self.doctor.id,
            'appointment_time': appointment_time.isoformat(),
            'reason': 'Routine checkup',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Accept either the serializer or model unique error message
        self.assertTrue(
            'This slot is already booked.' in str(response.data) or
            'The fields doctor, appointment_time must make a unique set.' in str(response.data),
            f"Unexpected error message: {response.data}"
        )

    def test_past_appointment_time(self):
        try:
            url = reverse('appointment-list')
        except Exception:
            url = '/api/appointments/my/'
        data = {
            'doctor': self.doctor.id,
            'appointment_time': (timezone.now() - timedelta(days=1)).isoformat(),
            'reason': 'Past appointment',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Appointment time must be in the future.', str(response.data))

    def test_update_appointment_status_and_notes(self):
        # Create appointment
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=2),
            reason='Initial',
        )
        appointment.status = 'CONFIRMED'
        appointment.notes = 'Bring previous reports.'
        appointment.save()
        updated = Appointment.objects.get(id=appointment.id)
        self.assertEqual(updated.status, 'CONFIRMED')
        self.assertEqual(updated.notes, 'Bring previous reports.')

    def test_appointment_duration_field(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=3),
            duration=45
        )
        self.assertEqual(appointment.duration, 45)

    def test_only_patient_can_update_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=4)
        )
        # Create another user
        other_user = User.objects.create_user(email='other@example.com', password='testpass123', full_name='Other User')
        self.client.force_authenticate(user=other_user)
        url = f"/appointments/{appointment.id}/"
        response = self.client.put(url, {'status': 'CANCELLED'}, format='json')
        # Should be forbidden or not allowed
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])



    def test_list_appointments_api(self):
        # Create two appointments
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=5),
            reason='A1'
        )
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=6),
            reason='A2'
        )
        try:
            url = reverse('appointment-list')
        except Exception:
            url = '/api/appointments/my/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_appointment_api(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=7),
            reason='Retrieve'
        )
        try:
            url = reverse('appointment-detail', args=[appointment.id])
        except Exception:
            url = f'/api/appointments/{appointment.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], appointment.id)

    def test_update_appointment_api(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=8),
            reason='Update'
        )
        try:
            url = reverse('appointment-detail', args=[appointment.id])
        except Exception:
            url = f'/api/appointments/{appointment.id}/'
        data = {'notes': 'Updated via API'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        appointment.refresh_from_db()
        self.assertEqual(appointment.notes, 'Updated via API')

    def test_delete_appointment_api(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_time=timezone.now() + timedelta(days=9),
            reason='Delete'
        )
        try:
            url = reverse('appointment-detail', args=[appointment.id])
        except Exception:
            url = f'/api/appointments/{appointment.id}/'
        response = self.client.delete(url)
        self.assertIn(response.status_code, [200, 204, 202, 204])
        self.assertFalse(Appointment.objects.filter(id=appointment.id).exists())