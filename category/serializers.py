from rest_framework import serializers
from .models import Category
from validators import validate_non_blank_title, validate_description, validate_title_null

class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200, validators=[validate_non_blank_title, validate_title_null])
    description = serializers.CharField(validators=[validate_description])

    class Meta:
        model = Category
        fields = ["id", "title", "slug", "description", "active"]
        
    def validate_slug(self, value):
        if value and len(value) > 200:
            raise serializers.ValidationError("O slug não pode ter mais de 200 caracteres.")
        return value
    
    def validate_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("O campo 'active' deve ser um valor booleano.")
        return value
        
    