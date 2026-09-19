from django.test import TestCase

from ..models import Order
from ..serializers import OrderSerializer, User


class OrderSerializerTestCase(TestCase):

    def test_serializer_user_exists(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {
            "user": user.pk,
            "quantity": 2,
            "total": 100.00,
            "status": "Pendente",
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_rejects_nonexistent_user(self):
        data = {
            "user": 999,  # Non-existent user ID
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


    def test_serializer_quantity_must_be_positive(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        data = {
            "user": user.pk,
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
            "quantity": 2,
            "total": 100.00,
            "status": "InvalidStatus",
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_serializer_has_expected_fields(self):
        user = User.objects.create_user(username="testuser", password="testpass")

        self.serializer = OrderSerializer()
        expected_fields = {"id", "user", "quantity", "total", "status"}
        self.assertEqual(set(self.serializer.fields.keys()), expected_fields)

    def test_serializer_return_expected_data(self):
        user = User.objects.create(username="adm", password="123")
        order = Order.objects.create(
            user=user, quantity=30, total="300.00", status="cancelado"
        )
        self.serializer = OrderSerializer(order)
        self.assertEqual(self.serializer.data["user"], order.id)
        self.assertEqual(self.serializer.data["quantity"], order.quantity)
        self.assertEqual(self.serializer.data["total"], order.total)
        self.assertEqual(self.serializer.data["status"], order.status)
