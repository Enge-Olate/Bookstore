from django.test import TestCase
from category.models import Category
from ..models import Product
from ..serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def test_serializer_acceptes_valid_data(self):
        category = Category.objects.create(title="Eletrônicos")
        data = {
            "title": "Teclado REdragon Kumara K552 RGB LED ABNT2",
            "description": "Teclado Mecânico Gamer Redragon Kumara K552 RGB LED ABNT2 Switch Outemu Blue, Black",
            "price": "280.00",
            "active": True,
            "category": [category.pk],
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_title(self):
        category = Category.objects.create(title = "Switches")
        data = {
            "description": "Teclado Mecânico Gamer Redragon Kumara K552 RGB LED ABNT2 Switch Outemu Blue, Black",
            "price": "280.00",
            "active": True,
            "category": [category.pk],
        }
        self.serializer = ProductSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("title", self.serializer.errors)

    def test_serializer_price_not_negative(self):
        category = Category.objects.create(title="Routers")
        data = {
            "title": "Teclado REdragon Kumara K552 RGB LED ABNT2",
            "description": "Teclado Mecânico Gamer Redragon Kumara K552 RGB LED ABNT2 Switch Outemu Blue, Black",
            "price": "-10.00",
            "active": True,
            "category": [category.pk],
        }
        self.serializer = ProductSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("price", self.serializer.errors)

    def test_serializer_create_product(self):
        category = Category.objects.create(title="Periféricos")
        data = {
            "title": "Mouse Gamer Logitech G203 RGB",
            "description": "Mouse gamer com sensor óptico.",
            "price": "160.00",
            "active": True,
            "category": [category.pk],
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()

        self.assertEqual(product.title, data["title"])
        self.assertEqual(product.category.get(), category)
