from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()


class ProductTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="admin@gmail.com",
            password="Pass@123"
        )

    def test_create_product(self):

        product = Product.objects.create(
            name="Laptop",
            price=50000,
            stock=5
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(Product.objects.count(), 1)