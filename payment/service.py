import stripe
from django.conf import settings
from django.urls import reverse

from borrowing.models import Borrowing
from payment.models import Payment


OVERDUE_COEFFICIENT = 2
stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_money_to_pay(borrowing: Borrowing):
    if borrowing.actual_return_date > borrowing.expected_return_date:
        overdue_days = (
            borrowing.actual_return_date - borrowing.expected_return_date
        ).days
        clean_days = (
            borrowing.expected_return_date - borrowing.borrow_date
        ).days
        count_of_money = (clean_days * borrowing.book.daily_fee) + (
            overdue_days * borrowing.book.daily_fee * 2
        )
        # result = (count_of_money, "FINE")
        # return result
        return count_of_money

    if borrowing.actual_return_date == borrowing.borrow_date:
        # result = (borrowing.book.daily_fee, "PAYMENT")
        # return result
        return borrowing.book.daily_fee

    clean_days = (borrowing.actual_return_date - borrowing.borrow_date).days
    # result = (clean_days * borrowing.book.daily_fee, "PAYMENT")
    # return result
    return clean_days * borrowing.book.daily_fee


def create_stripe_session(borrowing: Borrowing, request):
    money_to_pay = calculate_money_to_pay(borrowing)
    payment = Payment.objects.create(
        status="PENDING",
        type="PAYMENT",
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
