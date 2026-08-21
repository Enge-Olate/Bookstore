from django.db import models
from category.models import Category
class Product(models.Model):
    title = models.CharField(max_length=100, )
    description = models.TextField(max_length=500, null=True, blank=True)
    price= models.PositiveIntegerField(null=True)
    active = models.BooleanField(default=True)
    # Relacionamento
    category = models.ManyToManyField(Category, blank=True)