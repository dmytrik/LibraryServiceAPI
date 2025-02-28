from datetime import timedelta
from unittest.mock import MagicMock

from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingReturnBookSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


User = get_user_model()


class BorrowingSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.com", password="password123"
        )
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=1, daily_fee=1.0
        )
        self.context = {"request": self.client}
        self.client.force_authenticate(user=self.user)

    def test_borrowing_serializer_validation_no_active_borrowings(self):
        """Ensure validation passes when there are no active borrowings."""
        data = {
            "expected_return_date": (now().date() + timedelta(days=7)),
            "book": self.book.title,
        }

        mock_request = MagicMock()
        mock_request.user = self.user

        serializer = BorrowingSerializer(
            data=data, context={"request": mock_request}
        )
        self.assertTrue(serializer.is_valid())

    def test_borrowing_serializer_validation_with_active_borrowings(self):
        """Ensure validation fails if the user has active borrowings."""
        Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        data = {
            "expected_return_date": (now().date() + timedelta(days=14)),
            "book": self.book.title,
        }

        mock_request = MagicMock()
        mock_request.user = self.user

        serializer = BorrowingSerializer(
            data=data, context={"request": mock_request}
        )

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_borrowing_return_book_serializer(self):
        """Test BorrowingReturnBookSerializer handles return_book field correctly."""
        data = {"return_book": True}
        serializer = BorrowingReturnBookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["return_book"], True)

    def test_borrowing_list_serializer(self):
        """Test BorrowingListSerializer representation."""
        borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        serializer = BorrowingListSerializer(borrowing)
        expected_data = {
            "id": borrowing.id,
            "borrow_date": str(borrowing.borrow_date),
            "expected_return_date": str(borrowing.expected_return_date),
            "book": self.book.title,
            "payments": []
        }
        self.assertEqual(serializer.data, expected_data)

    def test_borrowing_list_serializer_excludes_actual_return_date(self):
        """Test BorrowingListSerializer excludes actual_return_date when not set."""
        borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        serializer = BorrowingListSerializer(borrowing)
        self.assertNotIn("actual_return_date", serializer.data)

    def test_borrowing_detail_serializer(self):
        """Test BorrowingDetailSerializer with BookSerializer representation."""
        borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        serializer = BorrowingDetailSerializer(borrowing)
        expected_data = {
            "id": borrowing.id,
            "borrow_date": str(borrowing.borrow_date),
            "expected_return_date": str(borrowing.expected_return_date),
            "book": {
                "id": self.book.id,
                "title": self.book.title,
                "author": self.book.author,
                "cover": "SOFT",
                "inventory": self.book.inventory,
                "daily_fee": "1.00",
                "unreturned_borrowings_count": 1,
            },
        }
        self.assertEqual(serializer.data, expected_data)
