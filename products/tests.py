from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class ProductAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vendor = User.objects.create_user(
            email="vendor1@example.com",
            username="vendor1",
            password="vendorpass123",
            user_type="vendor"
        )
        cls.customer = User.objects.create_user(
            email="customer1@example.com",
            username="customer1",
            password="customerpass123",
            user_type="customer"
        )
        cls.product = Product.objects.create(
            vendor=cls.vendor,
            name="Handmade Pottery",
            description="Beautiful pottery made by hand",
            price=50.00,
            stock=10
        )
        cls.list_url = reverse("product-list")

    def authenticate(self, user):
        """Attach JWT auth header for a given user"""
        tokens = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_vendor_can_create_product(self):
        self.authenticate(self.vendor)
        data = {
            "name": "New Basket",
            "description": "Handwoven basket",
            "price": 20.00,
            "stock": 5
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_customer_cannot_create_product(self):
        self.authenticate(self.customer)
        data = {
            "name": "Invalid Product",
            "description": "Should not be allowed",
            "price": 15.00,
            "stock": 3
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vendor_can_update_own_product(self):
        self.authenticate(self.vendor)
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.patch(url, {"price": 60.00}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(float(self.product.price), 60.00)

    def test_other_users_cannot_update_product(self):
        self.authenticate(self.customer)
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.patch(url, {"price": 100.00}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)