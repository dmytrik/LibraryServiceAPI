from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class CreateUserViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("user:create")
        self.user_data = {
            "email": "testuser@example.com",
            "password": "strongpassword",
            "is_staff": False,
        }

    def test_create_user_success(self):
        response = self.client.post(self.url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertNotIn("password", response.data)
