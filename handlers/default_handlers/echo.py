from telebot.types import Message # noqa

from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot_command = DEFAULT_COMMANDS + CUSTOM_COMMANDS
    text = [f"/{command} - {desk}" for command, desk in bot_command]
    text = "\n".join(text)
    bot.reply_to(
        message, "Я тебя не понимаю , я могу выполнять только команды."
                 f"Выбери одну из команд\n {text}"
    )
