from django.db import models

from book.models import Book
from django.conf import settings


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, related_name="borrowings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="borrowings")
