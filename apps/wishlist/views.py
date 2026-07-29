from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer
from apps.cart.models import Cart


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related("product")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=False, methods=["get"])
    def count(self, request):
        total = self.get_queryset().count()
        return Response({"wishlist_count": total})


    @action(detail=True, methods=["post"])
    def move_to_cart(self, request, pk=None):
        item = self.get_object()
        Cart.objects.create(user=request.user, product=item.product, quantity=1)
        item.delete()
        return Response({"message": "Moved To Cart"})