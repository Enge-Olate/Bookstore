from rest_framework import serializers

def validate_non_blank_title(value):
    if not value or not value.strip():
        raise serializers.ValidationError("Título não pode ser vazio.")
    return value

def validate_description(value):
    if value and len(value) > 500:
        raise serializers.ValidationError(
            "A descrição não pode ter mais de 500 caracteres."
        )
    return value

def validate_title_null(value):
    if value is None:
        raise serializers.ValidationError("O título não pode ser nulo.")
    return value