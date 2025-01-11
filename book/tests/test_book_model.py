from django.test import TestCase

from book.models import Book


class BookModelTest(TestCase):
    def test_book_creation(self):
        """Test the creation of a book with all fields"""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Cover.SOFT,
            inventory=5,
            daily_fee=10.00,
        )

        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.cover, Book.Cover.SOFT)
        self.assertEqual(book.inventory, 5)
        self.assertEqual(book.daily_fee, 10.00)

    def test_book_unique_title(self):
        """Test that the book title must be unique"""
        Book.objects.create(
            title="Unique Book",
            author="Author 1",
            cover=Book.Cover.SOFT,
            inventory=10,
            daily_fee=15.00,
        )

        with self.assertRaises(Exception):
            Book.objects.create(
                title="Unique Book",  # Same title
                author="Author 2",
                cover=Book.Cover.HARD,
                inventory=3,
                daily_fee=20.00,
            )
