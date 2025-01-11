from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from book.models import Book
from book.serializers import BookSerializer


class BookSerializerTest(APITestCase):
    def test_valid_book_data(self):
        """Test that valid book data passes through the serializer"""
        data = {
            "title": "Valid Book",
            "author": "Author 1",
            "cover": Book.Cover.HARD,
            "inventory": 5,
            "daily_fee": 10.00,
        }

        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.title, "Valid Book")

    def test_invalid_inventory(self):
        """Test that inventory cannot be negative"""
        data = {
            "title": "Invalid Inventory Book",
            "author": "Author 2",
            "cover": Book.Cover.SOFT,
            "inventory": -1,
            "daily_fee": 10.00,
        }

        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_daily_fee(self):
        """Test that daily fee must be greater than zero"""
        data = {
            "title": "Invalid Fee Book",
            "author": "Author 3",
            "cover": Book.Cover.HARD,
            "inventory": 3,
            "daily_fee": 0,
        }

        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
