from django.db import models

from book.models import Book
from django.conf import settings


class Borrowing(models.Model):
    """
    Borrowing model with attributes:
    borrow_date, expected_return_date, actual_return_date, book, user
    """

    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    def __str__(self):
        return str(self.borrow_date)
