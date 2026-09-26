from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from category.factories import CategoryFactories
from ..factories import ProductFactories

class ProductViewSetTestCase(APITestCase):
    def test_product_creation_without_categries(self):
        product = ProductFactories.create()
        self.assertEqual(product.category.count(), 0)
        
    def test_product_creation_categories(self):
        informatica = CategoryFactories(title = "Informática")
        saude_bem_estar = CategoryFactories(title = "Saúde e Bem Estar")
        product = ProductFactories.create(category = [informatica.id, saude_bem_estar.id])
        self.assertEqual(product.category.count(), 2)