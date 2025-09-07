from django.test import TestCase
from users.models import User 

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='strongpass123',
            user_type='customer'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('strongpass123'))
        self.assertEqual(user.user_type, 'customer')
    
    def test_create_vendor(self):
        vendor = User.objects.create_user(
            username='vendor1',
            email='vendor@example.com',
            password='vendorpass123',
            user_type='vendor'
        )
        self.assertEqual(vendor.user_type, 'vendor')