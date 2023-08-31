import os

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class SiteSettings(BaseSettings):
    BOT_TOKEN: SecretStr = os.getenv("BOT_TOKEN")
    RAPID_API_KEY: SecretStr = os.getenv("RAPID_API_KEY")
    HOST_API: SecretStr = os.getenv("HOST_API")


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)
