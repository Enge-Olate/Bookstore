import factory
from decimal import Decimal
from .models import Product
from category.factories import CategoryFactories


class ProductFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    title = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    price = Decimal("29.90")
    active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cat in extracted:
                self.category.add(cat)
        else:
            pass

