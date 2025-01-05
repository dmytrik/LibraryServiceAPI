from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrowing
from tg_bot.utils import send_telegram_notification


@receiver(post_save, sender=Borrowing)
def handle_borrowing_creation(instance, created, **kwargs):
    if created:
        message = (
            f"New borrowing for book: {instance.book.title}, "
            f" Expected return date: {instance.expected_return_date}"
        )
        send_telegram_notification.delay(message)
