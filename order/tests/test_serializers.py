from django.test import TestCase
from ..models import Order, OrderItem
from product.models import Product
from ..serializers import OrderSerializer, OrderItemSerializer, User


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


class OrderItemSerializerTestCase(TestCase):
    def test_serializer_accepts_valid_data(self):
        order = Order.objects.create(user=User.objects.create_user(username="testuser", password="testpass"), total=100.00, status="pending")
        product = Product.objects.create(title="Test Product", price=10.00)
        data = {
            "order": order.pk,
            "product": product.pk,
            "quantity": 2,
            "unit_price": 10.00,
            "subtotal": 20.00,
        }
        self.serializer = OrderItemSerializer(data= data)
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)

    def test_serializer_requires_quantity(self):
        order = Order.objects.create(user = User.objects.create_user(username="test", password = "123"))
        product = Product.objects.create(title="Paper clip", price = 2.00)
        data = {
            "order": order.pk,
            "product": product.pk,
            "unit_price": 2.00,
            "subtotal": 1000.00
        }
        self.serializer = OrderItemSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("quantity", self.serializer.errors)
        
    
    def test_serializer_subtotal_non_negative(self):
        order = Order.objects.create(user=User.objects.create_user(username="testuser", password="testpass"), total=100.00, status="pending")
        product = Product.objects.create(title="Test Product", price=10.00)
        data = {
            "order": order.pk,
            "product": product.pk,
            "quantity": 2,
            "unit_price": 10.00,
            "subtotal": -20.00,
        }
        self.serializer = OrderItemSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("subtotal", self.serializer.errors)

    def test_serializer_subtotal_matches_unit_price_times_quantity(self):
        order = Order.objects.create(user=User.objects.create_user(username="testuser", password="testpass"), total=100.00, status="pending")
        product = Product.objects.create(title="Test Product", price=10.00)
        data = {
            "order": order.pk,
            "product": product.pk,
            "quantity": 2,
            "unit_price": 10.00,
            "subtotal": 30.00,  # Incorrect subtotal
        }
        self.serializer = OrderItemSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("non_field_errors", self.serializer.errors)