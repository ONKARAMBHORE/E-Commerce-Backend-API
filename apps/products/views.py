from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.accounts.permissions import IsAdmin, IsSeller


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# viewset for brands

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
    permission_classes = [IsAuthenticated]


# product viewset

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        "category", "brand", "seller"
    ).prefetch_related(
        "images", "reviews"
    )

    permission_classes = [IsAuthenticated, IsAdmin | IsSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ["name", "description", "sku"]
    filterset_fields = ["category", "brand", "is_available"]
    ordering_fields = ["price", "created_at", "stock"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


# product imageviewset

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    permission_classes = [ IsAuthenticated ]



# review viewsets

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)