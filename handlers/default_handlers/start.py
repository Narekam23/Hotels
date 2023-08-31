from telebot.types import Message
from database.common.models import create_db
from loader import bot
from loguru import logger


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    create_db()
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
