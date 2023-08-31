from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def need_choice() -> InlineKeyboardMarkup:
    """Функцият создают просто кнопку да/нет"""
    keyboard = InlineKeyboardMarkup(row_width=2)

    button_one = InlineKeyboardButton('Да', callback_data='Да')
    button_two = InlineKeyboardButton('Нет', callback_data='Нет')

    keyboard.add(button_one, button_two)

    return keyboard
