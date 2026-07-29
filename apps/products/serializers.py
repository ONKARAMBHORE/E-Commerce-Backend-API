from rest_framework import serializers
from .models import *

# category serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# brand serializers
class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

# product image serializers

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary"]


# product serializers

class ProductSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True, read_only = True)

    class Meta:
        model = Product
        fields = "__all__"


# Review Serializers

class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields="__all__"
        read_only_fields=["user"]


# product detail serializers

class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = "__all__"

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()

        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)

        return 0