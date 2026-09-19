from django.test import TestCase
from ..models import Category
from ..serializers import CategorySerializer

class CategorySerializerTestCase(TestCase):

    def test_serializer_accepts_valid_data(self):
        data = {
            "title": "Eletrônicos",
            "slug": "eletronicos",
            "description": "Categoria de produtos eletrônicos",
            "active": True,
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_title(self):
        data = {
            "slug": "eletronicos",
            "description": "Categoria de produtos eletrônicos",
            "active": True,
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_serializer_requires_slug_is_optional(self):
        data = {
            "title": "Eletrônicos",
            "description": "Categoria de produtos eletrônicos",
            "active": True,
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())