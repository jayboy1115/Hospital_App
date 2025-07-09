from django.test import TestCase
from .models import ChatbotSession, ChatMessage
from patients.models import Patient
from authentication.models import User
from hospitals.models import Hospital, HospitalBranch

class ChatbotTests(TestCase):
    def setUp(self):
        import uuid
        unique_email = f"patient_{uuid.uuid4()}@example.com"
        unique_universal_id = f"P{uuid.uuid4().hex[:8]}"
        unique_hospital_email = f"hospital_{uuid.uuid4()}@example.com"
        unique_branch_name = f"Main Branch {uuid.uuid4().hex[:4]}"
        self.user = User.objects.create_user(email=unique_email, password='testpass123', full_name='Patient User')
        self.hospital = Hospital.objects.create(name='Test Hospital', email=unique_hospital_email, address='123 St', phone='1234567890')
        self.branch = HospitalBranch.objects.create(hospital=self.hospital, name=unique_branch_name, address='123 St', phone='1234567890', city='City', state='State')
        self.patient = Patient.objects.create(user=self.user, hospital_branch=self.branch, universal_id=unique_universal_id)
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

    def test_multiple_messages_and_order(self):
        messages = [
            ChatMessage.objects.create(session=self.session, sender='PATIENT', message=f'Message {i}')
            for i in range(5)
        ]
        retrieved = list(self.session.messages.order_by('timestamp'))
        self.assertEqual(len(retrieved), 5)
        self.assertEqual(retrieved[0].message, 'Message 0')
        self.assertEqual(retrieved[-1].message, 'Message 4')

    def test_session_with_suggested_drugs_and_recommendation(self):
        self.session.suggested_drugs = ['DrugA', 'DrugB']
        self.session.recommendation = 'Take DrugA after food.'
        self.session.save()
        updated = ChatbotSession.objects.get(id=self.session.id)
        self.assertIn('DrugA', updated.suggested_drugs)
        self.assertEqual(updated.recommendation, 'Take DrugA after food.')

    def test_delete_session_cascades_messages(self):
        ChatMessage.objects.create(session=self.session, sender='PATIENT', message='Test')
        session_id = self.session.id
        self.session.delete()
        self.assertFalse(ChatbotSession.objects.filter(id=session_id).exists())
        self.assertEqual(ChatMessage.objects.filter(session_id=session_id).count(), 0)

    def test_edge_cases(self):
        # Empty symptoms
        session = ChatbotSession.objects.create(patient=self.patient, symptoms='')
        self.assertEqual(session.symptoms, '')
        # Long message
        long_msg = 'x' * 1000
        msg = ChatMessage.objects.create(session=self.session, sender='PATIENT', message=long_msg)
        self.assertEqual(msg.message, long_msg)
