import os

from dotenv import find_dotenv, load_dotenv
from loguru import logger
from pydantic import BaseSettings, SecretStr, StrictStr

logger.add("debug.json", format="{time} {level} {module} {name} {message}", level="DEBUG", serialize=True)

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class SiteSettings(BaseSettings):
    BOT_TOKEN: SecretStr = os.getenv("BOT_TOKEN")
    RAPID_API_KEY: SecretStr = os.getenv("RAPID_API_KEY")
    HOST_API: StrictStr = os.getenv("HOST_API")


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку (показывает все команды бота"),
    ("low", "Показывает самые дешёвые отели в выбранном городе"),
    ("high", "Показывает самые дорогие отели в выбранном городе"),
    ("custom", "Поиск отеля по вашим параметрам"),
    ("history", "История запросов"),
)

CUSTOM_COMMANDS = (
    ("quiz", "Викторина"),
)
