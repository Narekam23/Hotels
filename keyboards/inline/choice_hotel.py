from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def choice_hotel(variants: List) -> InlineKeyboardMarkup:
    """Формирует список кнопки из списка отелей"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    for hotel in variants:
        button = InlineKeyboardButton(hotel[1], callback_data=hotel[0])
        keyboard.add(button)

    return keyboard
