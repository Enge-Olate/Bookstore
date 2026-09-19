from django.test import TestCase
from ..models import Category
from ..serializers import CategorySerializer

class CategorySerializerTestCase(TestCase):

    def test_serializer_accepts_valid_data(self):
        data = {
            "title": "Tecnologia da Informação",
            "slug": "Informatica",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        self.serializer = CategorySerializer(data=data)
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)

    def test_serializer_requires_title(self):
        data = {
            "slug": "Informatica",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        self.serializer = CategorySerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("title", self.serializer.errors)

    def test_serializer_allows_missing_slug(self):
        data = {

            "title": "Tecnologia da Informação",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        self.serializer = CategorySerializer(data=data)
        self.assertTrue(self.serializer.is_valid())
        
    def test_serializer_has_expected_fields(self):
        self.serializer = CategorySerializer()
        expected_fields = {"id", "title", "slug", "description", "active"}
        self.assertEqual(set(self.serializer.fields.keys()), expected_fields)


    def test_serializer_create_object(self):
        data = {
            "title": "Tecnologia da Informação",
            "slug": "Informatica",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        self.serializer = CategorySerializer(data=data)
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)
        category = self.serializer.save()
        self.assertIsInstance(category, Category)
        self.assertEqual(category.title, data["title"])
        self.assertEqual(category.slug, data["slug"])
        self.assertEqual(category.description, data["description"])
        self.assertEqual(category.active, data["active"])
        
    
    def test_serializer_reject_empty_title(self):
        data = {
            "title": "",
            "slug": "Informatica",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        self.serializer = CategorySerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("title", self.serializer.errors)
    
    def test_serializer_rejects_null_title(self):
            data = {
                "title": None,
                "slug": "informatica",
                "description": "Descrição",
                "active": True,
            }
    
            serializer = CategorySerializer(data=data)
    
            self.assertFalse(serializer.is_valid())
            self.assertIn("title", serializer.errors)
    
        
    def test_serializer_slug_invalid_characters(self):
        data = {
            "title": "Tecnologia da Informação",
            "slug": "Informática@#$%", 
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": True,
        }
        self.serializer = CategorySerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("slug", self.serializer.errors)
        
    def test_serializer_active_field_must_be_boolean(self):
        data = {
            "title": "Tecnologia da Informação",
            "slug": "Informatica",
            "description": "Editora O'Reilly, 2019. 1ª edição. 300 páginas.",
            "active": "sim",  
        }
        self.serializer = CategorySerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("active", self.serializer.errors)
        
        
    def test_serializer_returns_expected_data(self):
        category = Category.objects.create(
            title="Tecnologia da Informação",
            slug="informatica",
            description="Descrição",
            active=True,
        )

        serializer = CategorySerializer(category)

        self.assertEqual(serializer.data["title"], category.title)
        self.assertEqual(serializer.data["slug"], category.slug)
        self.assertEqual(serializer.data["description"], category.description)
        self.assertEqual(serializer.data["active"], category.active)