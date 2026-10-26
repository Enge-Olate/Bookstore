import factory
from decimal import Decimal
from .models import Product


class ProductFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    title = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    price = Decimal("1.00")
    active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.category.add(*extracted)
