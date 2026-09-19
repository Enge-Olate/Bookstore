from django.test import TestCase
from ..models import Category
from ..serializers import CategorySerializer

class CategorySerializerTestCase(TestCase):

    def test_serializer_accepts_valid_data(self):
        data = {
            "title": "Tecnologia da Informação",
            "slug": "Informática",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_title(self):
        data = {
            "slug": "Informática",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_serializer_requires_slug_is_optional(self):
        data = {

            "title": "Tecnologia da Informação",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())