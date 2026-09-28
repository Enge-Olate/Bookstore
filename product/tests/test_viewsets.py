from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from category.factories import CategoryFactories
from ..factories import ProductFactories
from ..models import Product

class ProductViewSetTestCase(APITestCase):
    def test_product_creation_without_categries(self):
        # Cria um product.
        product = ProductFactories.create()
        # verifica se há category.
        self.assertEqual(product.category.count(), 0)
        
    def test_product_creation_categories(self):
        # Cria duas categorias.
        informatica = CategoryFactories(title = "Informática")
        saude_bem_estar = CategoryFactories(title = "Saúde e Bem Estar")
        # Adiciona ao product.
        product = ProductFactories.create(category = [informatica.id, saude_bem_estar.id])
        # Verifica se as duas instancias de teste foram criadas no banco.
        self.assertEqual(product.category.count(), 2)
        
    def test_update_product(self):
        # Cria o product.title no banco.
        product = ProductFactories(title= "Mundo Velho")
        # Dados para atualizar.
        data = {"title": "Mundo Novo"}
        # A url.
        url = reverse("product-detail", kwargs={"pk":product.id})
        response = self.client.patch(url, data, format='json')
        # verifica sucesso.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Atualiza a instancia local.
        product.refresh_from_db()
        self.assertEqual(product.title, "Mundo Novo")
        
    def test_delete_product(self):
            # Cria a categoria no banco
            product = ProductFactories.create()
            
            url = reverse('product-detail', kwargs={'pk': product.id})
            response = self.client.delete(url)
            
            # Verifica status 204 (No Content - Padrão do DRF para delete)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            
            # Garante que a categoria foi apagada do banco
            self.assertEqual(Product.objects.count(), 0)
            
    def test_update_price(self):
        # Cria product.price no banco.
        product = ProductFactories.create(price = '0')
        # Dados para atualizar.
        data = {"price": '59.90'}
        # A url para atualizar.
        url = reverse("product-detail", kwargs={"pk": product.id})
        response = self.client.patch(url, data, format="json")
        # Verificação.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Atualiza a instancia local.
        product.refresh_from_db()
        self.assertEqual(product.price, Decimal('59.90'))
        
