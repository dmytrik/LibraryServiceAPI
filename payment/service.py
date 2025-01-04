import stripe
from django.conf import settings
from django.urls import reverse

from borrowing.models import Borrowing
from payment.models import Payment


OVERDUE_COEFFICIENT = 2
stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_money_to_pay(borrowing: Borrowing):
    """
    Calculate the amount of money to be paid based
    on the borrowing details.

    This function calculates the payment or fine
    amount depending on the following conditions:
    - If the book has not yet been returned
      (i.e., `actual_return_date` is None), it calculates the fee
      based on the number of days the book is expected to be borrowed.
    - If the book is returned late, a fine is applied based on
      the number of overdue days and the book's
      daily fee.
    - If the book is returned on time, no charge is applied.

    Args:
        borrowing (Borrowing): The borrowing object containing
        details of the book, borrowing dates, and fees.

    Returns:
        tuple: A tuple containing:
            - The calculated amount of money to be paid (float or int).
            - A string indicating the type of payment
            ("PAYMENT" for normal payments, "FINE" for fines, "ok" for no charge).
    """
    if not borrowing.actual_return_date:

        if borrowing.expected_return_date == borrowing.borrow_date:
            result = (borrowing.book.daily_fee, "PAYMENT")
            return result

        clean_days = (
            borrowing.expected_return_date - borrowing.borrow_date
        ).days
        count_of_money = clean_days * borrowing.book.daily_fee
        result = (count_of_money, "PAYMENT")
        return result

    if borrowing.actual_return_date > borrowing.expected_return_date:
        overdue_days = (
            borrowing.actual_return_date - borrowing.expected_return_date
        ).days

        count_of_money = overdue_days * borrowing.book.daily_fee * 2
        result = (count_of_money, "FINE")
        return result

    result = (0, "ok")
    return result

def create_stripe_session(borrowing: Borrowing, request):
    """
        Creates a Stripe checkout session for the given borrowing.

        This function calculates the money to pay for the borrowing using the
        `calculate_money_to_pay` function. If a payment or fine is applicable, it
        creates a new `Payment` object, initializes a Stripe checkout session,
        and returns the URL for the user to complete the payment.

        Args:
            borrowing (Borrowing): The borrowing object containing
            details of the book and payment information.
            request (HttpRequest): The HTTP request object, used
            to build absolute URLs for success and cancel URLs.

        Returns:
            str: A URL where the user can complete the payment via Stripe,
            or "ok" if no payment is required.
        """
    money_to_pay, _type = calculate_money_to_pay(borrowing)
    if _type == "ok":
        return _type
    payment = Payment.objects.create(
        status="PENDING",
        type=_type,
        borrowing=borrowing,
        money_to_pay=money_to_pay,
    )
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": borrowing.book.title,
                    },
                    "unit_amount": int(payment.money_to_pay * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("payment:payment-success") + f"?payment_id={payment.id}"
        ),
        cancel_url=request.build_absolute_uri(
            reverse("payment:payment-cancel") + f"?payment_id={payment.id}"
        ),
    )

    payment.session_url = session.url
    payment.session_id = session.id
    payment.save()
