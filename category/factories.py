import factory

from django.utils.text import slugify
from .models import Category

class CategoryFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("slug",)
    
    title = factory.Faker("catch_phrase")    
    description = factory.Faker("text", max_nb_chars=200)
    active = True


    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)    
