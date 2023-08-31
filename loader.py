from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data import config

base_config = config.SiteSettings()
storage = StateMemoryStorage()
bot = TeleBot(token=base_config.BOT_TOKEN.get_secret_value(), state_storage=storage)
