from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "title", "slug", "description", "active"]

    def validate_title(self, value):
        if value is None:
            raise serializers.ValidationError("O título não pode ser nulo.")
        if not value or not value.strip():
            raise serializers.ValidationError("Título não pode ser vazio.")
        return value

    def validate_description(self, value):
        if value is not None and len(value) > 500:
            raise serializers.ValidationError(
                "A descrição não pode ter mais de 500 caracteres."
            )
        return value

    def validate_slug(self, value):
        if value is not None and len(value) > 200:
            raise serializers.ValidationError(
                "O slug não pode ter mais de 200 caracteres."
            )
        return value

    def validate_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise serializers.ValidationError(
                "O campo 'active' deve ser um valor booleano."
            )
        return value
