from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.products.models import Category, Product

User = get_user_model()


class ProductTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="admin@gmail.com",
            password="Pass@123"
        )

    def test_create_product(self):

        category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        product = Product.objects.create(
            category=category,
            seller=self.user,
            name="Laptop",
            slug="laptop",
            description="A reliable laptop.",
            price=50000,
            stock=5,
            sku="LAPTOP-001",
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(Product.objects.count(), 1)