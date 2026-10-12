from decimal import Decimal

from rest_framework import serializers
from category.models import Category
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "category"]

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Título não pode ser vazio.")
        return value

    def validate_description(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError(
                "A descrição não pode ter mais de 500 caracteres."
            )
        return value

    def validate_price(self, value):
        if value is None:
            raise serializers.ValidationError("O preço não pode ser nulo.")
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        if value > Decimal("999999.99"):
            raise serializers.ValidationError(
                "O preço deve ser maior que zero e não pode ultrapassar 999999.99."
            )
        return value

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError(
                "O produto deve ter pelo menos uma categoria."
            )
        return value
