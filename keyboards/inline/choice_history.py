from typing import Dict

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def choice_history(database_dict: Dict) -> InlineKeyboardMarkup:
    """Функция которая формирует кнопку. Где кнопка - название отеля
    callback_data - подробная информация по отелю."""
    keyboard = InlineKeyboardMarkup(row_width=1)

    for row in database_dict:
        key = database_dict[row][1]['name']
        button = InlineKeyboardButton(key, callback_data=row)
        keyboard.add(button)

    return keyboard
