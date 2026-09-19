from django.test import TestCase
from category.models import Category
from ..models import Product
from ..serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def test_serializer_acceptes_valid_data(self):

        category = Category.objects.create(title="Tecnologia da Informação")
        data = {
            "title": "A cor dos Dados",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": "280.00",
            "active": True,
            "category": [category.pk],
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_title(self):

        category = Category.objects.create(title = "Informática")
        data = {
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "price": "280.00",
            "active": True,
            "category": [category.pk],
        }
        self.serializer = ProductSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("title", self.serializer.errors)

    def test_serializer_price_not_negative(self):
        category = Category.objects.create(title="Tecnologia da Informação")
        data = {
            "title": "A cor dos Dados",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": "-10.00",
            "active": True,
            "category": [category.pk],
        }
        self.serializer = ProductSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("price", self.serializer.errors)

    def test_serializer_create_product(self):
        category = Category.objects.create(title="Tecnologia da Informação")
        data = {
            "title": "A cor dos Dados",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": "280.00",
            "active": True,
            "category": [category.pk],
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()

        self.assertEqual(product.title, data["title"])
        self.assertEqual(product.category.get(), category)
