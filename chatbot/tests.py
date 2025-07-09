from django.test import TestCase
from .models import ChatbotSession, ChatMessage
from patients.models import Patient
from authentication.models import User
from hospitals.models import Hospital, HospitalBranch

class ChatbotTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='patient@example.com', password='testpass123', full_name='Patient User')
        self.hospital = Hospital.objects.create(name='Test Hospital', email='hospital@example.com', address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name='Main Branch', address='123 St', phone='1234567890', city='City', state='State')
        self.patient = Patient.objects.create(user=self.user, hospital_branch=self.branch, universal_id='P123')
        self.session = ChatbotSession.objects.create(patient=self.patient, symptoms='Cough and fever')

    def test_chatbot_session_creation(self):
        self.assertEqual(ChatbotSession.objects.count(), 1)
        self.assertEqual(self.session.patient, self.patient)
        self.assertEqual(self.session.symptoms, 'Cough and fever')

    def test_chat_message_flow(self):
        msg1 = ChatMessage.objects.create(session=self.session, sender='PATIENT', message='I have a headache')
        msg2 = ChatMessage.objects.create(session=self.session, sender='BOT', message='Take paracetamol')
        self.assertEqual(self.session.messages.count(), 2)
        self.assertEqual(msg1.sender, 'PATIENT')
        self.assertEqual(msg2.sender, 'BOT')
