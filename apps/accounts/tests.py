from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountTest(APITestCase):

    def test_register(self):

        data = {
            "email": "test@gmail.com",
            "password": "Pass@123",
            "first_name": "Om",
            "last_name": "Patil",
            "phone": "9876543210"
        }

        response = self.client.post(reverse("register"), data)


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):

        User.objects.create_user(
            email="test@gmail.com",
            password="Pass@123"
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "test@gmail.com",
                "password": "Pass@123"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)