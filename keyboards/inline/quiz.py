import random

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.common.models import Quiz, db


def quiz() -> (InlineKeyboardMarkup, str):
    """Создает кнопки для викторины"""
    count = [x for x in range(1, 193)]
    sampling = random.choices(count, k=4)
    object_list = list()
    with db:
        for num in sampling:
            db_object = Quiz.select().where(Quiz.id == num).get()
            object_list.append(db_object)

    question = object_list[0].question
    random.shuffle(object_list)
    keyboard = InlineKeyboardMarkup(row_width=2)

    button_list = list()

    for elem in object_list:
        if elem.question == question:
            button = InlineKeyboardButton(elem.answer, callback_data='1')
            button_list.append(button)
        else:
            button = InlineKeyboardButton(elem.answer, callback_data=2)
            button_list.append(button)

    button_cancel = InlineKeyboardButton('Выйти', callback_data='Выйти')
    keyboard.add(button_list[0], button_list[1])
    keyboard.add(button_list[2], button_list[3])
    keyboard.add(button_cancel)
    return keyboard, question
