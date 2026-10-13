<<<<<<< HEAD
import factory
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
=======
from decimal import Decimal

import factory
from django.contrib.auth import get_user_model
>>>>>>> origin/docker_network

from .models import Order

User = get_user_model()


<<<<<<< HEAD
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda number: f"order-user-{number}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.LazyFunction(lambda: make_password("test-password"))
=======
class UserFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "123456")
>>>>>>> origin/docker_network


class OrderFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
<<<<<<< HEAD

    user = factory.SubFactory(UserFactory)
    total = Decimal("1.00")
    quantity = 1
    status = "Pendente"

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if create and extracted:
            self.products.add(*extracted)
=======
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
>>>>>>> origin/docker_network
