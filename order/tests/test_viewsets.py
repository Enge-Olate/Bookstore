from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.factories import ProductFactories
from ..factories import OrderFactories, UserFactory
from ..models import Order


class OrderViewSetTestCase(APITestCase):
    def test_create_order(self):
        user = UserFactory(username="adm")
        product = ProductFactories()
        data = {
            "user": user.pk,
            "quantity": 2,
            "total": "1.00",
            "status": "Pendente",
            "products": [product.pk],
        }
        response = self.client.post(
            reverse("order-list"),
            data,
            format="json",
        )
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order.user, user)
        self.assertEqual(list(order.products.all()), [product])

    def test_create_order_without_user(self):
        product = ProductFactories()
        data = {
            "quantity": 2,
            "total": "1.00",
            "status": "Pendente",
            "products": [product.pk],
        }
        response = self.client.post(
            reverse("order-list"),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)

    def test_create_order_without_product(self):
        user = UserFactory(username="adm")
        data = {
            "user": user.pk,
            "quantity": 1,
            "total": "3.00",
            "status": "Pago",
            "product": [],
        }
        response = self.client.post(
            reverse("order-list"),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("products", response.data)
