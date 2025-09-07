from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.urls import reverse

class AuthAPITest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('refresh')
        
        self.user_data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'custpass123',
            'user_type': 'customer'
        }
        
        self.vendor_data = {
            'username': 'vendor1',
            'email':' vendor1@example.com',
            'password': 'vendorpass123',
            'user_type': 'vendor'
        }
    
    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'customer1')
    
    def test_user_login_and_jwt_tokens(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'username': 'customer1',
            'password': 'custpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_token_refresh(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'username': 'customer1',
            'password': 'custpass123'
        }, format='json')
        
        refresh_token = login_response.data['refresh']
        
        response = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)