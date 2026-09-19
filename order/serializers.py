from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Order

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )

    quantity = serializers.IntegerField(min_value=1, required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = ["id", "user", "quantity", "total", "status"]

    def to_internal_value(self, data):
        data = data.copy()
        if "status" in data and isinstance(data["status"], str):
            status_map = {
                "Pendente": "pending",
                "Processando": "processing",
                "Cancelado": "cancelled",
                "Pago": "paid",
            }
            data["status"] = status_map.get(data["status"], data["status"])
        return super().to_internal_value(data)

    def validate_product(self, value):
        if not value:
            raise serializers.ValidationError(
                "O pedido deve ter pelo menos um produto."
            )
        return value

    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError("O total não pode ser negativo.")
        return value

    def validate_status(self, value):
        status_map = {
            "pending": "pending",
            "processing": "processing",
            "cancelled": "cancelled",
            "paid": "paid",
        }
        valid_statuses = ["Pendente", "Processando", "Cancelado", "Pago"]

        if value not in status_map:
            raise serializers.ValidationError(
                f"O status deve ser um dos seguintes: {', '.join(valid_statuses)}."
            )

        return status_map[value]
