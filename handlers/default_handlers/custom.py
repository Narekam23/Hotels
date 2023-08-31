import datetime
import json

import peewee
from loguru import logger
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery

from API_site.core import site_api, utils_func, url, headers, querystring, payload_list, payload_detail
from database.common.models import History
from keyboards.inline.Calendar import Calendar, CallbackData
from keyboards.inline.choice_city import choice_city
from keyboards.inline.choice_hotel import choice_hotel
from keyboards.inline.choice import need_choice
from loader import bot
from states.contact_information import UserInfoState

calendar = Calendar()
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


@bot.message_handler(commands=["custom"])
def city_name(message: Message) -> None:
    """Запрашиваем название города."""
    logger.info("Запускается команда 'custom'")

    bot.set_state(message.from_user.id,
                  UserInfoState.city_name_custom,
                  message.chat.id
                  )

    bot.send_message(message.from_user.id,
                     f'{message.from_user.full_name}. Введи название города.'
                     )


@bot.message_handler(state=UserInfoState.city_name_custom)
def get_city_name(message: Message) -> None:
    """Функция выводит кнопки состоящие из совпадение и просит уточнить город"""
    if message.text.isalpha():
        logger.info("Запускается функция")

        try:
            search = site_api.locations_search()
            payload = querystring
            payload['q'] = message.text
            logger.info("Отправляем API запрос")
            response = search(url, headers, payload, timeout=5)

            if response.status_code == 200:
                logger.info('Запрос прошёл успешно')
            else:
                logger.error("Неуспешный запрос!")

            data = json.loads(response.text)

            if len(data['sr']) > 0:
                sorted_city = utils_func.cities_dict()
                city_dict = sorted_city(data['sr'])
                markup = choice_city(city_dict)

                with bot.retrieve_data(message.from_user.id) as data:
                    data['city_dict'] = city_dict

                bot.send_message(message.chat.id,
                                 'Уточните пожалуйста город или район.',
                                 reply_markup=markup)

            else:
                bot.send_message(message.from_user.id,
                                 'Вы ввели несуществующий  город')

            logger.info("Функция выполнилась")

        except (AttributeError, KeyError, TypeError):
            logger.error("При выполении функции произошла одна из ошибок: "
                         "AttributeError, KeyError, TypeError")

    else:
        bot.send_message(message.from_user.id,
                         'Некорректное название')
        bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=UserInfoState.city_name_custom)
def callback(call):
    """Callback функция.
    Запрашиваем количество взрослых"""
    if call.message:

        with bot.retrieve_data(call.from_user.id) as data:
            data['city_id'] = call.data

            for key in data['city_dict'].keys():
                if data['city_dict'][key] == call.data:
                    data['region'] = key
                    bot.edit_message_text(f'вы выбрали {key}',
                                          call.message.chat.id,
                                          call.message.message_id
                                          )

        bot.set_state(call.from_user.id, UserInfoState.count_adults_custom)
        bot.send_message(call.message.chat.id, "Введите количество взрослых")


@bot.message_handler(state=UserInfoState.count_adults_custom)
def get_adults(message: Message) -> None:
    """ Функция выводит календарь и просит ввести дату заезда"""
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data['adults'] = message.text

        now = datetime.datetime.now()
        bot.send_message(

            message.chat.id,
            "Выберите дату заезда",
            reply_markup=calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,
            ),
        )
        bot.set_state(message.from_user.id,
                      UserInfoState.arrival_date_custom,
                      message.chat.id
                      )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix),
    state=UserInfoState.arrival_date_custom)
def callback_inline(call: CallbackQuery):
    """ Функция выводит календарь и просит ввести дату выезда"""
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(
        bot=bot,
        call=call,
        name=name,
        action=action,
        year=year,
        month=month,
        day=day
    )
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Вы выбрали {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )

        with bot.retrieve_data(call.from_user.id) as data:
            data['arrival_date'] = date.strftime('%d.%m.%Y')

        now = datetime.datetime.now()
        bot.send_message(
            call.message.chat.id,
            "Выберите дату выезда",
            reply_markup=calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,
            ),
        )
        bot.set_state(call.from_user.id, UserInfoState.departure_date_custom)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix),
    state=UserInfoState.departure_date_custom)
def callback_inline(call: CallbackQuery):
    """Функция проверяет корректность введённой даты и запрашивает минимальную сумму"""
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(
        bot=bot,
        call=call,
        name=name,
        action=action,
        year=year,
        month=month,
        day=day
    )
    if action == "DAY":
        date_comparison = utils_func.date_comparison()

        with bot.retrieve_data(call.from_user.id) as data:
            answer = date_comparison(data['arrival_date'], date.strftime('%d.%m.%Y'))

            if answer:
                data['departure_date'] = date.strftime('%d.%m.%Y')
                bot.send_message(

                    chat_id=call.from_user.id,
                    text=f"Вы выбрали {date.strftime('%d.%m.%Y')}",
                    reply_markup=ReplyKeyboardRemove(),
                )
                bot.send_message(call.from_user.id,
                                 "Введите минимальную сумму"
                                 )
                bot.set_state(call.from_user.id, UserInfoState.min_price)
            else:
                now = datetime.datetime.now()
                bot.send_message(

                    call.message.chat.id,
                    "Дата заезда не может быть раньше даты выезда!\nВыберите дату выезда",
                    reply_markup=calendar.create_calendar(
                        name=calendar_1_callback.prefix,
                        year=now.year,
                        month=now.month,
                    ),
                )


@bot.message_handler(state=UserInfoState.min_price)
def min_price(message: Message) -> None:
    """Функция запрашивает максимальную сумму"""
    if message.text.isdigit():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min'] = message.text

        bot.set_state(message.from_user.id,
                      UserInfoState.max_price,
                      message.chat.id)
        bot.send_message(message.from_user.id, 'Введите максимальную сумму')

    else:
        bot.send_message(message.from_user.id, 'Сумма должна состоять только из цифр')


@bot.message_handler(state=UserInfoState.max_price)
def min_price(message: Message) -> None:
    """Запрашивает количество отелей которые хочет увидеть пользователь"""
    if message.text.isdigit():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max'] = message.text

        bot.set_state(message.from_user.id,
                      UserInfoState.count_hotels_custom,
                      message.chat.id)
        bot.send_message(message.from_user.id, "Какое количество отелей показать?(макс. 5шт)")

    else:
        bot.send_message(message.from_user.id, 'Сумма должна состоять только из цифр')


@bot.message_handler(state=UserInfoState.count_hotels_custom)
def get_count(message: Message) -> None:
    """Функция выводит все отели и краткую информацию по ним.
    Выводит кнопки с названием отелей и предлагает пользователю выбрать отель."""
    if int(message.text) <= 5 and message.text.isdigit():
        logger.info("Запускается функция")
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

                payload = payload_list
                create_payload = utils_func.new_payload()
                new_payload = create_payload(payload=payload,
                                             data=data)

                search = site_api.properties_list()
                logger.info("Отправляем API запрос")
                response = search(url, headers, new_payload, timeout=15)

                if response.status_code == 200:
                    logger.info('Запрос прошёл успешно')
                else:
                    logger.error("Неуспешный запрос!")

                data_file = json.loads(response.text)

                try:
                    hotels_list_info = data_file['data']['propertySearch']['properties']

                    sorted_func = utils_func.sorted_info()
                    sorted_info = sorted_func(hotels_list_info, int(message.text))

                    search = site_api.properties_detail()
                    payload = payload_detail
                    info_dict = dict()

                    logger.info('Запускается цикл')

                    for hotel in sorted_info:

                        payload['propertyId'] = hotel[0]
                        logger.info("Отправляем API запрос")
                        response = search(url, headers, payload, timeout=10)

                        if response.status_code == 200:
                            logger.info('Запрос прошёл успешно')
                        else:
                            logger.error("Неуспешный запрос!")

                        hotels_data = json.loads(response.text)

                        find_photo_func = utils_func.find_photo()
                        find_photo = find_photo_func(hotels_data)
                        info_dict[payload['propertyId']] = [payload['propertyId'],
                                                            hotel[1],
                                                            hotel[2],
                                                            find_photo[0],
                                                            hotel[3],
                                                            find_photo[1]]

                        bot.send_photo(message.from_user.id, find_photo[1])
                        bot.send_message(message.from_user.id,
                                         "Отель: '{hotel_name}.'\n"
                                         "Стоимость: '{price}$.'\n"
                                         "Адрес: '{address}.'\n"
                                         "Расстояние до центра: {destination}км.".format(
                                             hotel_name=hotel[1],
                                             price=hotel[2],
                                             address=find_photo[0],
                                             destination=hotel[3])
                                         )
                        logger.info('Цикл завершился успешно')
                        data['info_dict'] = info_dict

                    markup = choice_hotel(sorted_info)
                    bot.send_message(message.chat.id,
                                     'Выберите отель, чтобы узнать более детальную информацию ',
                                     reply_markup=markup)
                    bot.set_state(message.from_user.id,
                                  UserInfoState.choice_hotel_custom,
                                  message.chat.id)

                except TypeError:
                    bot.send_message(message.from_user.id, "По вашим параметрам ничего не найдено.\n"
                                                           "/custom - Нажмите чтобы попробовать снова "
                                                           "/help - Нажмите чтобы выбрать другую команду")

            logger.info("Функция выполнилась")

        except (AttributeError, KeyError, TypeError):
            logger.error("При выполении функции произошла одна из ошибок: "
                         "AttributeError, KeyError, TypeError")

            bot.send_message(message.from_user.id,
                             'По вашим параметрам ничего не найдено.'
                             'Попробуйте изменить параметры')
            bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы ввели недопустимое количество отелей')


@bot.callback_query_handler(func=lambda call: True, state=UserInfoState.choice_hotel_custom)
def callback(call):
    """Функция показывает подробную информацию по выбранному отелю
        и запрашивает у пользователя хочет ли он увидеть допольнительные фото и информацию"""
    if call.message:
        logger.info("Запускается функция")

        try:
            payload = payload_detail
            payload['propertyId'] = call.data

            search = site_api.properties_detail()
            logger.info("Отправляем API запрос")
            response = search(url, headers, payload, timeout=10)

            if response.status_code == 200:
                logger.info('Запрос прошёл успешно')
            else:
                logger.error("Неуспешный запрос!")

            data = json.loads(response.text)

            hotel_info_func = utils_func.property_sorted()
            hotel_info = hotel_info_func(data)

            with bot.retrieve_data(call.from_user.id) as data:

                info_list = list()
                info = data['info_dict']

                for list_hotel in info.values():
                    if list_hotel[0] == call.data:
                        info_list = list_hotel

                hotel_info['name'] = info_list[1]
                hotel_info['address'] = info_list[3]
                hotel_info['destination'] = info_list[4]
                hotel_info['price'] = info_list[2]
                hotel_info['photo'] = info_list[5]

                data['hotel_info'] = hotel_info

                bot.edit_message_text(

                    "Подробная информация по отелю\n"
                    "Название отеля: {name}.\n"
                    "Адрес: {address}.\n"
                    "Расстояние до центра города: {destination}км.\n"
                    "Количество звёзд: {star}.\n"
                    "Рейтинг: {rating}.\n"
                    "Стоимость: {price}$.\n"
                    "Дополнительная информация: {info}\n".format(
                        name=hotel_info['name'],
                        address=hotel_info['address'],
                        destination=hotel_info['destination'],
                        star=hotel_info['stars'],
                        rating=hotel_info['rating'][0],
                        price=info_list[2],
                        info=','.join(hotel_info['info'])  # изм
                    ),
                    call.message.chat.id,
                    call.message.message_id
                )
            markup = need_choice()
            bot.send_message(call.from_user.id,
                             'Показать дополнительные фотографии по выбранному отелю?',
                             reply_markup=markup)
            bot.set_state(call.from_user.id, UserInfoState.photo_custom)

            logger.info("Функция выполнилась")

        except (AttributeError, KeyError, TypeError):
            logger.error("При выполении функции произошла одна из ошибок: "
                         "AttributeError, KeyError, TypeError")


@bot.callback_query_handler(func=lambda call: True, state=UserInfoState.photo_custom)
def callback(call):
    """Функция Показывает дополнительные фото и записывает выбор пользователя в базу данных"""
    logger.info("Запускается функция")
    text = "/help"

    if call.data == 'Нет':
        bot.reply_to(call.message, f"{text} - Нажмите чтобы выбрать другую команду")

    else:

        with bot.retrieve_data(call.from_user.id) as data:
            for info in data['hotel_info']['images']:
                bot.send_photo(call.message.chat.id, info[1])
                bot.send_message(call.message.chat.id, info[0])
    bot.reply_to(call.message, f"{text} - Нажмите чтобы выбрать другую команду")

    with bot.retrieve_data(call.from_user.id) as data:

        region = data['region']
        hotel_info = data['hotel_info']
        logger.info("Начинается запись в базу данных")

        try:
            History.create(
                telegram_id=call.message.chat.id,
                region=region,
                name=hotel_info['name'],
                address=hotel_info['address'],
                destination=hotel_info['destination'],
                star=hotel_info['stars'],
                rating=hotel_info['rating'][0],
                info=','.join(hotel_info['info']),
                photo=hotel_info['photo'],
                datatime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            logger.info("Запись в базу данных прошла успешно")
            logger.info("Команда 'custom' завершена")

        except peewee.PeeweeException:
            logger.error("При записи в базу данных произошла ошибка PeeweeException")
