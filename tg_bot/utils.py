import os
import asyncio

from celery import shared_task
from telegram import Bot


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@shared_task
def send_telegram_notification(message):
    bot = Bot(token=BOT_TOKEN)
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=message))
