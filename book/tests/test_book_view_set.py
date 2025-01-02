from rest_framework import status
from rest_framework.test import APITestCase
from book.models import Book


class BookViewSetTest(APITestCase):

    def setUp(self):
        """Create a test book entry before tests"""
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Cover.SOFT,
            inventory=5,
            daily_fee=10.00
        )

    def test_create_book(self):
        """Test creating a book via the API"""
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.Cover.HARD,
            "inventory": 5,
            "daily_fee": 12.00
        }
        response = self.client.post("/api/book-service/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_read_book(self):
        """Test retrieving a book via the API"""
        response = self.client.get(f"/api/book-service/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        """Test updating a book via the API"""
        data = {
            "inventory": 10,  # Перевірка нового значення inventory
            "title": self.book.title,  # Титул залишається незмінним
            "author": self.book.author,  # Автор залишається незмінним
            "cover": self.book.cover,  # Обкладинка залишається незмінною
            "daily_fee": self.book.daily_fee,  # Залишаємо попереднє значення daily_fee
        }
        response = self.client.put(f"/api/book-service/books/{self.book.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 10)

    def test_delete_book(self):
        """Test deleting a book via the API"""
        response = self.client.delete(f"/api/book-service/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())