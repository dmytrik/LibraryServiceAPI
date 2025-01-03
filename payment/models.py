from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    """
    Represents a payment or fine associated with a borrowing transaction.

    This model tracks the status and type of payments, linking them to specific
    borrowings. Payments can be marked as pending or paid, and can either represent
    a standard payment or a fine.

    Attributes:
        status (str): The current status of the payment (PENDING or PAID).
        type (str): The type of payment (PAYMENT or FINE).
        borrowing (Borrowing): The borrowing record this payment is associated with.
        session_url (str, optional): URL for the payment session (e.g., Stripe session).
        session_id (str, optional): Identifier for the payment session.
        money_to_pay (Decimal): The amount to be paid or fined, with up to 10 digits
                                and 2 decimal places.

    Meta:
        ordering (list): Orders the payments by the borrowing date in descending order.

    Methods:
        __str__(): Returns a human-readable string representation of the payment,
                   showing the user's email, amount, and payment status.
    """

    class Status(models.TextChoices):
        """
        Enum-like class for defining possible statuses of a payment.

        Attributes:
            PENDING (str): Payment is pending.
            PAID (str): Payment is completed.
        """

        PENDING = ("PENDING",)
        PAID = ("PAID",)

    class Type(models.TextChoices):
        """
        Enum-like class for defining possible types of payments.

        Attributes:
            PAYMENT (str): Standard payment for borrowing.
            FINE (str): Fine for late return or damage.
        """

        PAYMENT = ("PAYMENT",)
        FINE = ("FINE",)

    status = models.CharField(
        max_length=7, choices=Status, default=Status.PENDING
    )
    type = models.CharField(max_length=7, choices=Type, default=Type.PAYMENT)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=500, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-borrowing__borrow_date"]

    def __str__(self):
        return f"{self.borrowing.user.email} - {self.money_to_pay} USD - {self.status}"
