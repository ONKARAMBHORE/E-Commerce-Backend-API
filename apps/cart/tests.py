from rest_framework.test import APITestCase

class CartTest(APITestCase):

    def test_cart_api(self):

        response = self.client.get("/api/cart/")

        self.assertIn(response.status_code, [200, 401])