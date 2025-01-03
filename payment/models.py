from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = ("PENDING",)
        PAID = ("PAID",)

    class Type(models.TextChoices):
        PAYMENT = ("PAYMENT",)
        FINE = ("FINE",)

    status = models.CharField(
        max_length=7,
        choices=Status,
        default=Status.PENDING
    )
    type = models.CharField(
        max_length=7,
        choices=Type,
        default=Type.PAYMENT
    )
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=500, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-borrowing__borrow_date"]

    def __str__(self):
        return f"{self.borrowing.user.email} - {self.money_to_pay} USD - {self.status}"
