from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class UserManagerTests(TestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "password123"

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email=self.email, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password=self.password)

    def test_create_user_with_invalid_email(self):
        invalid_email = "invalid_email"
        user = get_user_model().objects.create_user(
            email=invalid_email, password=self.password
        )
        self.assertEqual(user.email, invalid_email.lower())

    def test_create_superuser_with_no_is_staff(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=self.email, password=self.password, is_staff=False
            )

    def test_create_superuser_with_no_is_superuser(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=self.email, password=self.password, is_superuser=False
            )

    def test_user_email_uniqueness(self):
        get_user_model().objects.create_user(email=self.email, password=self.password)
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email=self.email, password="newpassword123"
            )

    def test_user_email_case_insensitivity(self):
        user1 = get_user_model().objects.create_user(
            email="TESTUSER@EXAMPLE.COM", password=self.password
        )
        user2 = get_user_model().objects.create_user(
            email="testuser@example.com", password=self.password
        )
        self.assertEqual(user1.email.lower(), user2.email.lower())
