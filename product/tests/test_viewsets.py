from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from category.factories import CategoryFactories
from ..factories import ProductFactories
from ..models import Product


class ProductViewSetTestCase(APITestCase):
    def test_create_product_with_categories(self):
        category = CategoryFactories.create(title="Informática")
        data = {
            "title": "Mundo Novo",
            "price": "59.90",
            "category": [category.pk],
        }

        response = self.client.post(reverse("product-list"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(pk=response.data["id"])
        self.assertEqual(product.title, data["title"])
        self.assertEqual(list(product.category.all()), [category])

    def test_create_product_without_categories_returns_validation_error(self):
        data = {
            "title": "Mundo Novo",
            "price": "59.90",
            "category": [],
        }

        response = self.client.post(reverse("product-list"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category", response.data)

    def test_update_product(self):
        product = ProductFactories(title="Mundo Velho")
        data = {"title": "Mundo Novo"}
        url = reverse("product-detail", kwargs={"pk": product.pk})

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.title, "Mundo Novo")

    def test_delete_product(self):
        product = ProductFactories.create()
        url = reverse("product-detail", kwargs={"pk": product.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_update_price(self):
        product = ProductFactories.create()
        data = {"price": "59.90"}
        url = reverse("product-detail", kwargs={"pk": product.pk})

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.price, Decimal("59.90"))

    def test_update_price_above_limit_returns_validation_error(self):
        product = ProductFactories.create()
        url = reverse("product-detail", kwargs={"pk": product.pk})

        response = self.client.patch(url, {"price": "1000000.00"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)
