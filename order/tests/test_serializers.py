from django.test import TestCase

from ..models import Order
from ..serializers import OrderSerializer, User


class OrderSerializerTestCase(TestCase):
    
    def test_serializer_user_exists(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {
            "user": user.pk,
            "product": [1, 2],
            "quantity": 2,
            "total": 100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
    def test_serializer_rejects_nonexistent_user(self):
        data = {
            "user": 999,  # Non-existent user ID
            "product": [1, 2],
            "quantity": 2,
            "total": 100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
    
    
    def test_serializer_requires_user(self):
        data = {"product": [1, 2], "quantity": 2, "total": 100.00, "status": "Pendente"}
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_serializer_requires_product(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {"user": user.pk, "quantity": 2, "total": 100.00, "status": "Pendente"}
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_serializer_quantity_must_be_positive(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {
            "user": user.pk,
            "product": [1, 2],
            "quantity": -1,
            "total": 100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_serializer_total_must_not_be_negative(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {
            "user": user.pk,
            "product": [1, 2],
            "quantity": 2,
            "total": -100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("total", serializer.errors)

    def test_serializer_status_must_be_valid(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {
            "user": user.pk,
            "product": [1, 2],
            "quantity": 2,
            "total": 100.00,
            "status": "InvalidStatus",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)


