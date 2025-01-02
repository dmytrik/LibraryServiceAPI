from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD",
        SOFT = "SOFT",

    title = models.CharField(max_length=63, unique=True)
    author = models.CharField(max_length=63)
    cover = models.CharField(
        max_length=4,
        choices=Cover,
        default=Cover.SOFT,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
