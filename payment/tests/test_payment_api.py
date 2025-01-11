from datetime import timedelta

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.test import APITestCase
from rest_framework import status

from book.models import Book
from borrowing.models import Borrowing
from payment.models import Payment
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer


PAYMENT_URL = reverse("payment:payments-list")


def get_retrieve_payment_url(payment_id: int):
    """
    Generate URL for retrieving a specific payment by ID.

    Args:
        payment_id (int): ID of the payment to retrieve.

    Returns:
        str: URL to access the payment detail endpoint.
    """
    return reverse("payment:payments-detail", args=(payment_id,))


class UnauthenticatedPaymentApiTest(APITestCase):
    """
    Test suite for unauthenticated access to the payment API.
    """

    def test_auth_required(self):
        """
        Ensure authentication is required to access the payment API.
        """
        response = self.client.get(PAYMENT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentApiTest(APITestCase):
    """
    Test suite for authenticated user interactions with the payment API.
    """

    def setUp(self):
        """
        Set up initial data for tests, including users, books,
        borrowings, and payments.
        """
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test1234"
        )
        self.second_user = get_user_model().objects.create_user(
            email="secon@mail.com", password="second1234"
        )
        self.first_book = Book.objects.create(
            title="first_test_book",
            author="first_test_author",
            cover="SOFT",
            inventory=7,
            daily_fee=3,
        )
        self.second_book = Book.objects.create(
            title="second_test_book",
            author="second_test_author",
            cover="HARD",
            inventory=7,
            daily_fee=3,
        )
        self.borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.first_book,
            user=self.user,
        )
        self.second_borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=10),
            book=self.second_book,
            user=self.second_user,
        )
        self.first_payment = Payment.objects.create(
            borrowing=self.borrowing, money_to_pay=10
        )
        self.second_payment = Payment.objects.create(
            borrowing=self.second_borrowing, money_to_pay=15
        )
        self.client.force_authenticate(self.user)

    def test_list_payment(self):
        """
        Test that authenticated users can retrieve a list of their own payments.
        """
        response = self.client.get(PAYMENT_URL)
        payments = Payment.objects.filter(borrowing__user=self.user)
        serializer = PaymentListSerializer(payments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_payment(self):
        """
        Test that authenticated users can retrieve the details of their specific payments.
        """
        url = get_retrieve_payment_url(self.first_payment.id)
        response = self.client.get(url)
        serializer = PaymentDetailSerializer(self.first_payment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_not_your_payment_rejected(self):
        """
        Test that users cannot retrieve payments that do not belong to them.
        """
        url = get_retrieve_payment_url(self.second_payment.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminPaymentApiTest(APITestCase):
    """
    Test suite for admin interactions with the payment API.
    """

    def setUp(self):
        """
        Set up data for admin tests, including admin and regular users,
        books, borrowings, and payments.
        """
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test1234"
        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test1234"
        )
        self.first_book = Book.objects.create(
            title="first_test_book",
            author="first_test_author",
            cover="SOFT",
            inventory=7,
            daily_fee=3,
        )
        self.second_book = Book.objects.create(
            title="second_test_book",
            author="second_test_author",
            cover="HARD",
            inventory=7,
            daily_fee=3,
        )
        self.borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=7),
            book=self.first_book,
            user=self.admin,
        )
        self.second_borrowing = Borrowing.objects.create(
            expected_return_date=now().date() + timedelta(days=10),
            book=self.second_book,
            user=self.user,
        )
        self.first_payment = Payment.objects.create(
            borrowing=self.borrowing, money_to_pay=10
        )
        self.second_payment = Payment.objects.create(
            borrowing=self.second_borrowing, money_to_pay=15
        )
        self.client.force_authenticate(self.admin)

    def test_all_payments_allowed(self):
        """
        Test that admin users can retrieve all payments in the system.
        """
        payments = Payment.objects.all()
        response = self.client.get(PAYMENT_URL)
        serializer = PaymentListSerializer(payments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
