from telebot.types import Message

from keyboards.inline.quiz import quiz
from loader import bot
from states.contact_information import UserInfoState


@bot.message_handler(commands=["quiz"])
def get_history(message: Message) -> None:
    """Отправляет пользователю страну и кнопки с вариантами ответа"""
    markup, question = quiz()
    bot.send_message(message.chat.id,
                     "Добро пожаловать в викторину 'Угадай столицу'",
                     )
    bot.send_message(message.chat.id,
                     question,
                     reply_markup=markup,
                     )
    bot.set_state(message.from_user.id,
                  UserInfoState.quiz,
                  message.chat.id
                  )


@bot.callback_query_handler(func=lambda call: True, state=UserInfoState.quiz)
def callback(call):
    """Сallback функция"""
    markup, question = quiz()

    if call.data == '1':
        bot.edit_message_text("Правильно",
                              call.message.chat.id,
                              call.message.message_id,
                              )
        bot.send_message(call.message.chat.id,
                         question,
                         reply_markup=markup,
                         )

    elif call.data == 'Выйти':
        bot.delete_state(call.message.from_user.id, call.message.chat.id)
        bot.edit_message_text("Чтобы выбрать другую команду нажмите /help",
                              call.message.chat.id,
                              call.message.message_id,
                              )

    else:
        bot.edit_message_text("Неправильно",
                              call.message.chat.id,
                              call.message.message_id,
                              )
        bot.send_message(call.message.chat.id,
                         question,
                         reply_markup=markup,
                         )
