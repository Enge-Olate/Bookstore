from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Category
from ..factories import CategoryFactories

class CategoryViewSetTestCase(APITestCase):
    
    def test_list_categories(self):
        # Gera 5 categorias de uma só vez e salva no banco de dados de teste
        CategoryFactories.create_batch(5)
        
        # Faz uma requisição GET para a rota de listagem
        url = reverse('category-list')
        response = self.client.get(url)
        
        # Verifica se a requisição foi um sucesso e se retornou as 5 categorias
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve_category(self):
        # Cria uma única categoria no banco
        category = CategoryFactories.create()
        
        # Faz uma requisição GET para os detalhes daquela categoria específica
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.get(url)
        
        # Verifica se o endpoint retornou os dados corretos
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], category.title)
        self.assertEqual(response.data['slug'], category.slug)

    def test_create_category(self):
        # Usamos .build() porque NÃO queremos salvar no banco ainda.
        # Queremos apenas gerar dados válidos para enviar no payload da requisição POST.
        category_payload = CategoryFactories.build()
        data = {
            "title": category_payload.title,
            "description": category_payload.description,
            "active": category_payload.active
        }
        
        url = reverse('category-list')
        response = self.client.post(url, data, format='json')
        
        # Verifica se foi criado (201) e se agora existe 1 registro no banco
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        
        # Verifica se o banco salvou com o título que enviamos
        saved_category = Category.objects.first()
        self.assertEqual(saved_category.title, data['title'])

    def test_update_category(self):
        # Cria a categoria original no banco
        category = CategoryFactories.create(title="Título Antigo")
        
        # Dados para atualização (PATCH)
        data = {"title": "Título Novo"}
        
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.patch(url, data, format='json')
        
        # Verifica sucesso
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Atualiza a instância local pegando do banco e verifica a mudança
        category.refresh_from_db()
        self.assertEqual(category.title, "Título Novo")

    def test_delete_category(self):
        # Cria a categoria no banco
        category = CategoryFactories.create()
        
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.delete(url)
        
        # Verifica status 204 (No Content - Padrão do DRF para delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Garante que a categoria foi apagada do banco
        self.assertEqual(Category.objects.count(), 0)