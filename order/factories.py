import factory
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .models import Order

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda number: f"order-user-{number}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.LazyFunction(lambda: make_password("test-password"))


class OrderFactories(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total = Decimal("1.00")
    quantity = 1
    status = "Pendente"

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if create and extracted:
            self.products.add(*extracted)
