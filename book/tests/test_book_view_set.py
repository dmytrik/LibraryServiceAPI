from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from book.models import Book

User = get_user_model()


class BookViewSetTest(APITestCase):
    def setUp(self):
        """Set up test data before running tests"""
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Cover.SOFT,
            inventory=5,
            daily_fee=10.00,
        )

        # Create a superuser using the custom user model
        self.superuser = User.objects.create_superuser(
            email="admin@example.com", password="admin123"
        )

        # Create a regular user using the custom user model
        self.user = User.objects.create_user(
            email="user@example.com", password="user123"
        )

    def test_list_books_unauthenticated(self):
        """Test: Unauthenticated users can view the list of books"""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book_unauthenticated(self):
        """Test: Unauthenticated users can view book details"""
        response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book_as_superuser(self):
        """Test: Superusers can create new books"""
        self.client.force_authenticate(user=self.superuser)
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.Cover.HARD,
            "inventory": 5,
            "daily_fee": 12.00,
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_create_book_as_regular_user(self):
        """Test: Regular users cannot create new books"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.Cover.HARD,
            "inventory": 5,
            "daily_fee": 12.00,
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_superuser(self):
        """Test: Superusers can update book details"""
        self.client.force_authenticate(user=self.superuser)
        data = {
            "inventory": 10,
            "title": self.book.title,
            "author": self.book.author,
            "cover": self.book.cover,
            "daily_fee": self.book.daily_fee,
        }
        response = self.client.put(
            f"/api/books/{self.book.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 10)

    def test_update_book_as_regular_user(self):
        """Test: Regular users cannot update book details"""
        self.client.force_authenticate(user=self.user)
        data = {
            "inventory": 10,
            "title": self.book.title,
            "author": self.book.author,
            "cover": self.book.cover,
            "daily_fee": self.book.daily_fee,
        }
        response = self.client.put(
            f"/api/books/{self.book.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_as_superuser(self):
        """Test: Superusers can delete books"""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_as_regular_user(self):
        """Test: Regular users cannot delete books"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
