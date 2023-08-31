from typing import Dict

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def choice_city(variants: Dict) -> InlineKeyboardMarkup:
    """Функция которая выводит кнопку. Кнопка - Название района.
    callback_data - id"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for key in variants.keys():
        button = InlineKeyboardButton(key, callback_data=variants[key])
        keyboard.add(button)

    return keyboard
