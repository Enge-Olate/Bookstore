from decimal import Decimal

import factory
from django.contrib.auth import get_user_model

from .models import Order

User = get_user_model()


class UserFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "123456")


class OrderFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactories)
    total = Decimal("0.00")
    quantity = 1
    status = "pending"

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for product in extracted:
                self.products.add(product)
        else:
            pass