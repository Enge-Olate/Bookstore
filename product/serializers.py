from rest_framework import serializers
from category.models import Category
from .models import Product
from validators import validate_non_blank_title, validate_description

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200, validators=[validate_non_blank_title])
    description = serializers.CharField(validators=[validate_description])
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "category"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value

    
    def validate_decimal_price(self, value):
        if value is not None and (value < 0 or value > 999999.99):
            raise serializers.ValidationError("O preço deve estar entre 0 e 999999.99.")
        return value

    

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError(
                "O produto deve ter pelo menos uma categoria."
            )
        return value
