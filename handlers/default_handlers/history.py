from loader import bot
from states.contact_information import UserInfoState
from database.common.models import History
from telebot.types import Message
from database.Utils.Database_funcs import DatabaseUtils
from keyboards.inline.choice import need_choice
from keyboards.inline.choice_history import choice_history


@bot.message_handler(commands=["history"])
def get_history(message: Message) -> None:
    """Функция отправляет пользователю его историю запросов.
    И предлагает выбор показать доп информацию или нет."""
    if len(History.select()) == 0:
        bot.send_message(message.from_user.id, "Ваша история запросов пустая")

    else:
        database_create = DatabaseUtils.create_history_dict()
        database_dict = database_create(History, message.from_user.id)

        create_text = DatabaseUtils.create_history_text()
        text = create_text(database_dict)
        bot.send_message(message.from_user.id, text)
        bot.send_message(message.from_user.id,
                         "Показать подробную инфомарцию по отелю ?",
                         reply_markup=need_choice()
                         )
        bot.set_state(message.from_user.id,
                      UserInfoState.choice_history,
                      message.chat.id
                      )


@bot.callback_query_handler(func=lambda call: True, state=UserInfoState.choice_history)
def callback(call):
    """Callback функция. Отпралвяет пользователю кнопки, которые содержат отели"""
    if call.data == "Нет":
        text = "/help"
        bot.reply_to(call.message, f"{text} - Нажмите чтобы выбрать другую команду")

    else:

        database_create = DatabaseUtils.create_history_dict()
        database_dict = database_create(History, call.from_user.id)
        keyboard = choice_history(database_dict)

        bot.send_message(call.message.chat.id,
                         "Выберите отель",
                         reply_markup=keyboard)
        bot.set_state(call.from_user.id, UserInfoState.choice_city_history)


@bot.callback_query_handler(func=lambda call: True, state=UserInfoState.choice_city_history)
def callback(call):
    """callback функция. Показывает подробную информацию по выбраному отелю из истории"""
    database_create = DatabaseUtils.create_history_dict()
    database_dict = database_create(History, call.from_user.id)

    create_text = DatabaseUtils.create_text()

    text, photo = create_text(database_dict, call.data)

    bot.send_photo(call.from_user.id, photo)
    bot.send_message(call.from_user.id, text)
