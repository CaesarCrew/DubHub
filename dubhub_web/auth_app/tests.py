from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from auth_app.forms import SignupForm

class TestLogin(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        
        # Create a test user
        self.user = User.objects.create_user(
            email='admin@example.com',
            user_type=4,
            password='123456789'
        )
    
    
    def test_login_success(self):
        response = self.client.post(self.login_url, data = {'email' : 'admin@example.com', 'password' : '123456789'})
        self.assertEqual(response.status_code, 200)
        #self.assertRedirects(response, reverse('home'))

class TestSignup(TestCase):
    def test_signup(self):
        url = reverse('signup')
        data = {
            'email' : 'testuser@example.com',
            'password' : '123456789',
            'first_name' : 'Test',
            'last_name' : 'User',
            'user_type' : 4
        }
        response = self.client.post(url, data)
        form = SignupForm(data=data)
        #self.assertTrue(form.is_valid())
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, data['email'])

class TestLogout(TestCase):
    def test_logout(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

class TestAPILogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='123456789',
            user_type=4,
            is_active=True
        )

    def test_login_api(self):
        url = reverse('api_login')  # certifique-se de que este nome está correto no urls.py
        data = {
            'username': 'admin@example.com',  # DRF espera 'username' por padrão
            'password': '123456789'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], self.user.email)