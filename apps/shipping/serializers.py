from rest_framework import serializers
from .models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):  # Address serializer
    class Meta:
        model = ShippingAddress          # Shipping model
        fields = "__all__"               # All fields
        read_only_fields = ["user"]      # User not editable