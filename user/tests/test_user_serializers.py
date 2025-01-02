from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from user.serializers import UserSerializer


class UserSerializerTest(APITestCase):
    def setUp(self):
        self.password = "password123"
        self.user_data = {
            "email": "testuser@example.com",
            "password": self.password,
            "is_staff": False,
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)

    def test_update_user(self):
        user = get_user_model().objects.create_user(
            email="existinguser@example.com", password="oldpassword"
        )
        new_data = {"email": "newemail@example.com", "password": "newpassword123"}

        serializer = UserSerializer(user, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, new_data["email"])
        self.assertTrue(updated_user.check_password(new_data["password"]))

    def test_update_user_without_password(self):
        user = get_user_model().objects.create_user(
            email="existinguser@example.com", password="oldpassword"
        )
        new_data = {"email": "newemail@example.com"}

        serializer = UserSerializer(user, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, new_data["email"])
        self.assertTrue(updated_user.check_password("oldpassword"))

    def test_password_is_write_only(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com", password="password123"
        )

        serializer = UserSerializer(user)
        self.assertNotIn("password", serializer.data)

    def test_create_user_with_existing_email(self):
        get_user_model().objects.create_user(
            email="testuser@example.com", password=self.password
        )

        data = {
            "email": "testuser@example.com",
            "password": self.password,
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
