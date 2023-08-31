from telebot.types import BotCommand

from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS


def set_default_commands(bot):
    bot_commands = DEFAULT_COMMANDS + CUSTOM_COMMANDS
    bot.set_my_commands(
        [BotCommand(*i) for i in bot_commands]
    )
