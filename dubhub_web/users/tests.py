from django.test import TestCase
from django.urls import reverse

from .models import User

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user@example.com', '123456789', first_name='Test User 0', is_active=True)
    
    def test_user_creation(self):
        user = User.objects.create_user('user1@example.com', '123456789', first_name='Test User', is_active=True)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=user.id).email, 'user1@example.com')
        self.assertEqual(user.first_name, 'Test User')
    
    def test_user_delete(self):
        user_id = self.user.id
        self.user.delete()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(User.objects.filter(id=user_id).exists(), False)
    
    def test_user_update(self):
        user = User.objects.get(id=self.user.id)
        user.first_name = 'Updated User'
        user.save()

        self.assertEqual(User.objects.get(id=self.user.id).first_name, 'Updated User')
    
    def test_user_get(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(User.objects.get(id=self.user.id).first_name, 'Test User 0')
        self.assertEqual(User.objects.get(id=self.user.id).email, 'user@example.com')

class TestPhotoUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user@example.com', '123456789', first_name='Test User 0', is_active=True, photo='users/fotos/1746213107142350.jpg')

    def test_user_photo(self):
        user = User.objects.get(id=self.user.id)
        url = reverse('foto-user', kwargs={'arquivo': '1746213107142350.jpg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')