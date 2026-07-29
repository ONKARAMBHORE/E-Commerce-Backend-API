from rest_framework.test import APITestCase

class PaymentTest(APITestCase):

    def test_payment_history(self):

        response = self.client.get("/api/payments/")

        self.assertIn(response.status_code, [200, 401])