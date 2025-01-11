import datetime

from celery import shared_task

from tg_bot.utils import send_telegram_notification
from borrowing.models import Borrowing


@shared_task
def send_message():
    """
    Celery task to send reminders for overdue borrowings.

    This task checks for borrowings that are overdue (expected return date has passed)
    and have not yet been returned. For each overdue borrowing, it sends a Telegram
    notification to remind the user.

    The notification includes details such as the user's name, book title, borrow date,
    and the number of days the borrowing is overdue.

    Args:
        None

    Returns:
        None
    """

    today = datetime.date.today()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=today,
        actual_return_date__isnull=True
    )
    for borrowing in overdue_borrowings:
        message = (
            f"📚 Borrowing Overdue Reminder ‼️\n"
            f"User: {borrowing.user.username}\n"
            f"Book: {borrowing.book.title}\n"
            f"Borrow Date: {borrowing.borrow_date}\n"
            f"Expected Return Date: {borrowing.expected_return_date}\n"
            f"Overdue by: {today - borrowing.expected_return_date} days\n"
        )
        send_telegram_notification.delay(message)
