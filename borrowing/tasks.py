import datetime

from celery import shared_task
from tg_bot.utils import send_telegram_notification

from borrowing.models import Borrowing


@shared_task
def send_message():
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
