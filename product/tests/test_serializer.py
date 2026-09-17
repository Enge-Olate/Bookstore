from django.test import TestCase
from ..models import Product
from ..serializers import ProductSerializer



class ProductSerializerTestCase(TestCase):
    def test_serializer_acceptes_valid_data(self):
        data={
            "title": "Teclado REdragon Kumara K552 RGB LED ABNT2",
                            "description": "Teclado Mecânico Gamer Redragon Kumara K552 RGB LED ABNT2 Switch Outemu Blue, Black",
                            "price": "280.00",
                            "active": True,
                            "category": [],
                    
        }
        self.serializer = ProductSerializer(data=data)
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)

    def test_serializer_requires_title(self):
        data={"description": "Teclado Mecânico Gamer Redragon Kumara K552 RGB LED ABNT2 Switch Outemu Blue, Black",
                        "price": "280.00",
                        "active": True,
                        "category": [],}
        self.serializer = ProductSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("title", self.serializer.errors)

    def test_serializer_price_not_negative(self):
        data={"title": "Teclado REdragon Kumara K552 RGB LED ABNT2",
            "description": "Teclado Mecânico Gamer Redragon Kumara K552 RGB LED ABNT2 Switch Outemu Blue, Black",
            "price": "-10.00",
            "active": True,
            "category": [],}
        self.serializer = ProductSerializer(data=data)
        self.assertFalse(self.serializer.is_valid())
        self.assertIn("price", self.serializer.errors)
        
    def test_serializer_create_product(self):
        data={
            "title": "Mouse Gamer Logitech G203 RGB",
            "price": "160.00",
            "active": True,
            "category": [],
        }
        self.serializer = ProductSerializer(data=data)
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)
        product = self.serializer.save()
        self.assertEqual(product.title, data["title"])
        self.assertEqual(Product.objects.count(), 1)
        self.assertTrue(product.active)
        