from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from borrowing.models import Borrowing, Book


User = get_user_model()


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.com", password="password123"
        )
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=1, daily_fee=1
        )
        self.expected_return_date = now().date() + timedelta(days=7)
        self.borrowing = Borrowing.objects.create(
            expected_return_date=self.expected_return_date,
            book=self.book,
            user=self.user,
        )

    def test_borrowing_creation(self):
        """Test if Borrowing object is created properly."""
        self.assertEqual(Borrowing.objects.count(), 1)
        borrowing = Borrowing.objects.first()
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(
            borrowing.expected_return_date, self.expected_return_date
        )
        self.assertIsNone(borrowing.actual_return_date)
        self.assertEqual(borrowing.borrow_date, now().date())

    def test_str_method(self):
        """Test the __str__ method of Borrowing."""
        borrowing = Borrowing.objects.first()
        self.assertEqual(str(borrowing), str(borrowing.borrow_date))

    def test_book_relation(self):
        """Test the ForeignKey relation with Book."""
        self.assertEqual(self.book.borrowings.count(), 1)
        self.assertIn(self.borrowing, self.book.borrowings.all())

    def test_user_relation(self):
        """Test the ForeignKey relation with User."""
        self.assertEqual(self.user.borrowings.count(), 1)
        self.assertIn(self.borrowing, self.user.borrowings.all())

    def test_actual_return_date_blank(self):
        """Test that actual_return_date can be blank."""
        self.borrowing.actual_return_date = now().date()
        self.borrowing.save()
        self.assertEqual(self.borrowing.actual_return_date, now().date())
