from rest_framework import serializers
from django.contrib.auth import get_user_model
from product.models import Product
from .models import Order, OrderItem

User = get_user_model()

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    
    
    product = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=True,
        allow_empty=False,
    )
    quantity = serializers.IntegerField(min_value=1, required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = ["id", "user", "product", "quantity", "total", "status"]
        
    
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
            raise serializers.ValidationError("O pedido deve ter pelo menos um produto.")
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


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "unit_price", "subtotal"]

    def validate_product(self, value):
        if not value:
            raise serializers.ValidationError("O pedido deve ter pelo menos um produto.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

    def validate_subtotal(self, value):
        if value < 0:
            raise serializers.ValidationError("O subtotal não pode ser negativo.")
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço unitário não pode ser negativo.")
        return value

    def validate_order(self, value):
        if not value:
            raise serializers.ValidationError(
                "O item do pedido deve estar associado a uma ordem de pedido."
            )
        return value
    
    def validate(self, attrs):
        expected_subtotal = attrs["unit_price"] * attrs["quantity"]
        
        if attrs["subtotal"] != expected_subtotal:
            raise serializers.ValidationError(
                "O subtotal não corresponde ao preço unitário multiplicado pela quantidade."
            )
        return attrs