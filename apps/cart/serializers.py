from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ["id", "product", "product_name", "product_price", "quantity", "subtotal"]