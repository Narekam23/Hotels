from telebot.types import Message
from database.common.models import create_db
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    create_db()
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
