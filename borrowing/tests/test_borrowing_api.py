from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from book.models import Book
from borrowing.models import Borrowing

User = get_user_model()

class BorrowingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@user.com", password="password123")
        self.staff_user = User.objects.create_user(email="test@admin.com", password="adminpassword", is_staff=True)
        self.book = Book.objects.create(title="Test Book", author="Author", inventory=5, daily_fee=1)
        self.client.force_authenticate(user=self.user)

    def test_create_borrowing(self):
        """Test creating a borrowing record."""
        data = {
            "expected_return_date": (now().date() + timedelta(days=7)),
            "book": self.book.title,
        }
        url = reverse("borrowing:borrowings-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)
        self.assertEqual(Borrowing.objects.first().user, self.user)

    def test_create_borrowing_no_inventory(self):
        """Test creating a borrowing record when no copies are available."""
        self.book.inventory = 0
        self.book.save()

        data = {
            "expected_return_date": (now().date() + timedelta(days=7)),
            "book": self.book.title,
        }
        url = reverse("borrowing:borrowings-list")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_borrowings_for_user(self):
        """Test retrieving the list of borrowings for the authenticated user."""
        borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        url = reverse("borrowing:borrowings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], borrowing.id)

    def test_list_borrowings_for_staff(self):
        """Test retrieving the list of borrowings for an admin user."""
        self.client.force_authenticate(user=self.staff_user)
        Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        url = reverse("borrowing:borrowings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_return_book(self):
        """Test returning a borrowed book."""
        self.book.inventory = 5
        self.book.save()

        borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        response = self.client.post(f"/api/borrowings/{borrowing.id}/return/")
        borrowing.refresh_from_db()
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsNotNone(borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 6)

    def test_return_book_already_returned(self):
        """Test trying to return a book that has already been returned."""
        borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
            actual_return_date=now(),
        )
        response = self.client.post(f"/api/borrowings/{borrowing.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "This borrowing has already been returned.")

    def test_permission_denied_for_non_authenticated_user(self):
        """Test that non-authenticated users are denied access."""
        self.client.logout()
        url = reverse("borrowing:borrowings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
