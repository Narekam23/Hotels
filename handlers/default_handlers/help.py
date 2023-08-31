from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    bot_command = DEFAULT_COMMANDS + CUSTOM_COMMANDS
    text = [f"/{command} - {desk}" for command, desk in bot_command]
    bot.reply_to(message, "\n".join(text))
