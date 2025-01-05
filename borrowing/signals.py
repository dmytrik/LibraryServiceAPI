from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrowing
from tg_bot.utils import send_telegram_notification


@receiver(post_save, sender=Borrowing)
def handle_borrowing_creation(instance, created, **kwargs):
    """
    Signal handler to send a notification when a new Borrowing instance is created.

    This function listens for the post_save signal of the Borrowing model. If a new
    borrowing record is created, it sends a Telegram notification with the book title
    and expected return date.

    Args:
        instance (Borrowing): The instance of Borrowing that was saved.
        created (bool): Indicates if the instance was created (True) or updated (False).
        **kwargs: Additional keyword arguments.

    """
    if created:
        message = (
            f"New borrowing for book: {instance.book.title}, "
            f" Expected return date: {instance.expected_return_date}"
        )
        send_telegram_notification.delay(message)
