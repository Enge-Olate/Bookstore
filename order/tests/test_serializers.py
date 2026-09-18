from django.test import TestCase
from ..models import Order
from ..serializers import OrderSerializer


class OrderSerializerTestCase(TestCase):
    def test_serializer_accepts_valid_data(self):
        data = {
            "user": 1,
            "product": [1, 2],
            "quantity": 2,
            "total": 100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_user(self):
        data = {"product": [1, 2], "quantity": 2, "total": 100.00, "status": "Pendente"}
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_serializer_requires_product(self):
        data = {"user": 1, "quantity": 2, "total": 100.00, "status": "Pendente"}
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_serializer_quantity_must_be_positive(self):
        data = {
            "user": 1,
            "product": [1, 2],
            "quantity": -1,
            "total": 100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_serializer_total_must_not_be_negative(self):
        data = {
            "user": 1,
            "product": [1, 2],
            "quantity": 2,
            "total": -100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("total", serializer.errors)

    def test_serializer_status_must_be_valid(self):
        data = {
            "user": 1,
            "product": [1, 2],
            "quantity": 2,
            "total": 100.00,
            "status": "InvalidStatus",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
