from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.factories import ProductFactories

from ..factories import OrderFactories, UserFactory
from ..models import Order


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="adm")
        self.product = ProductFactories()
        self.valid_data = {
            "user": self.user.pk,
            "quantity": 2,
            "total": "100.00",
            "status": "Pendente",
            "products": [self.product.pk],
        }

    def post_order(self, data):
        return self.client.post(reverse("order-list"), data, format="json")

    def test_create_order(self):
        response = self.post_order(self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total, Decimal("100.00"))
        self.assertEqual(order.status, "pending")
        self.assertEqual(list(order.products.all()), [self.product])

    def test_create_order_without_user(self):
        data = self.valid_data.copy()
        data.pop("user")

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)

    def test_create_order_with_nonexistent_user(self):
        data = {**self.valid_data, "user": self.user.pk + 1000}

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)

    def test_create_order_without_products(self):
        data = self.valid_data.copy()
        data.pop("products")

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("products", response.data)

    def test_create_order_with_empty_products(self):
        data = {**self.valid_data, "products": []}

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["products"][0]),
            "O pedido deve ter pelo menos um produto.",
        )

    def test_create_order_with_nonexistent_product(self):
        data = {**self.valid_data, "products": [self.product.pk + 1000]}

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("products", response.data)

    def test_create_order_with_zero_quantity(self):
        data = {**self.valid_data, "quantity": 0}

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_create_order_with_negative_total(self):
        data = {**self.valid_data, "total": "-1.00"}

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("total", response.data)

    def test_create_order_with_invalid_status(self):
        data = {**self.valid_data, "status": "Inválido"}

        response = self.post_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_update_order(self):
        order = Order.objects.create(
            user=self.user,
            quantity=2,
            total=Decimal("100.00"),
            status="pending",
        )
        order.products.add(self.product)
        url = reverse("order-detail", kwargs={"pk": order.pk})

        response = self.client.patch(url, {"total": "120.00"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.total, Decimal("120.00"))

    def test_delete_order(self):
        order = Order.objects.create(
            user=self.user,
            quantity=2,
            total=Decimal("100.00"),
            status="pending",
        )
        url = reverse("order-detail", kwargs={"pk": order.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())
