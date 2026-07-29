from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related("product")

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]

        item = Cart.objects.filter(user=self.request.user, product=product).first()

        if item:
            item.quantity += serializer.validated_data["quantity"]
            item.save()
            return

        serializer.save(user=self.request.user)

# update quantity
    @action(detail=True, methods=["patch"])
    def update_quantity(self, request, pk=None):
        cart = self.get_object()

        quantity = int(request.data.get("quantity", 1))

        if quantity < 1:
            raise ValidationError({"quantity": "Must be greater than 0"})

        cart.quantity = quantity
        cart.save()

        return Response(CartSerializer(cart).data)

# clear cart
    @action(detail=False, methods=["delete"])
    def clear(self, request):
        self.get_queryset().delete()
        return Response({"message": "Cart Cleared"})


#   Cart Summary
    @action(detail=False, methods=["get"])
    def summary(self, request):
        items = self.get_queryset()

        total_price = sum(item.subtotal for item in items)

        total_quantity = items.aggregate(Sum("quantity"))["quantity__sum"] or 0

        return Response({
            "items": CartSerializer(items, many=True).data,
            "total_quantity": total_quantity,
            "total_price": total_price
    })


    