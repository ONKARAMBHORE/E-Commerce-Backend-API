from rest_framework.test import APITestCase

class OrderTest(APITestCase):

    def test_orders(self):

        response = self.client.get("/api/orders/")

        self.assertIn(response.status_code, [200, 401])