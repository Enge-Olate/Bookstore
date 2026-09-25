import factory
from .models import Category
from serializers import CategorySerializer

class CategoryFactories(factory.django.DjangoModelFactory):
    class Meta:
        category = Category.title
    
    title = "livros"
        