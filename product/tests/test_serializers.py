from django.test import TestCase
from category.models import Category
from category.serializers import CategorySerializer
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
        self.assertEqual(product.category.all()[0], category)

    def test_serializer_non_existent_category(self):
        data = {
            "title": "A cor dos Dados",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": "280.00",
            "active": True,
            "category": [999],  # Non-existent category ID
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)
        
    def test_serializer_has_expected_fields(self):
        self.serializer = ProductSerializer()
        expected_fields = {"id", "title", "description", "price", "active", "category"} 
        self.assertEqual(set(self.serializer.fields.keys()), expected_fields)
        
    def test_serializer_reject_empty_title(self):
        category = Category.objects.create(title="Tecnologia da Informação")
        data = {
            "title": "",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": "280.00",
            "active": True,
            "category": [category.pk],
        }
        self.serializer = ProductSerializer(data=data)
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
        
    
    def test_serializer_requires_category(self):
        data = {
            "title": "Livro",
            "description": "Descrição",
            "price": "100.00",
            "active": True,
            "category": [],
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)
        
    
    def test_serializer_missing_category(self):
        data = {
            "title": "Livro",
            "description": "Descrição",
            "price": "100.00",
            "active": True,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)
            
    
    def test_serializer_rejects_non_numeric_price(self):
        category = Category.objects.create(title="Tecnologia da Informação")
        data = {
            "title": "A cor dos Dados",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": "abc",  # Non-numeric price
            "active": True,
            "category": [category.pk],
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)
        
    def test_serializer_rejects_price_null(self):
        category = Category.objects.create(title="Tecnologia da Informação")
        data = {
            "title": "A cor dos Dados",
            "description": "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            "price": None, 
            "active": True,
            "category": [category.pk],
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)
        
        
    def test_serializer_return_expected_data(self):
        category = Category.objects.create(title = "TI")
        product = Product.objects.create(
            title = "A Cor dos Dados",
            description = "Editora Novatec, 2019. 1ª edição. 256 páginas.",
            price = "280.00",
            active = True,
        )
        product.category.add(category)
        
        self.serializer = ProductSerializer(product)
        self.assertEqual(self.serializer.data["title"], product.title)
        self.assertEqual(self.serializer.data["description"], product.description)
        self.assertEqual(self.serializer.data["price"], product.price)
        self.assertEqual(self.serializer.data["active"], product.active)