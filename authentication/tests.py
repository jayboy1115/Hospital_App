from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


class UserAuthTests(APITestCase):
    def test_user_registration_with_profile_image(self):
        url = reverse('register')
        # Create a valid in-memory image
        image_io = BytesIO()
        image = Image.new('RGB', (10, 10), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
        data = {
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'password': 'testpass123',
            'profile_image': image_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_user_login(self):
        user = User.objects.create_user(email='loginuser@example.com', password='testpass123', full_name='Login User')
        url = reverse('login')
        data = {'email': 'loginuser@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_detail_and_update(self):
        user = User.objects.create_user(email='detailuser@example.com', password='testpass123', full_name='Detail User')
        self.client.force_authenticate(user=user)
        url = reverse('user-detail')
        # GET user detail
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'detailuser@example.com')
        # PUT update user
        response = self.client.put(url, {'full_name': 'Updated Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Updated Name')
