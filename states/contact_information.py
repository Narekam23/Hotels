from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """Класс содержит состояния пользователя"""

    city_name_low = State()
    count_adults_low = State()
    count_hotels_low = State()
    arrival_date_low = State()
    choice_hotel_low = State()
    departure_date_low = State()
    photo_low = State()

    city_name_high = State()
    count_adults_high = State()
    count_hotels_high = State()
    arrival_date_high = State()
    choice_hotel_high = State()
    departure_date_high = State()
    photo_high = State()

    city_name_custom = State()
    count_adults_custom = State()
    count_hotels_custom = State()
    arrival_date_custom = State()
    choice_hotel_custom = State()
    min_price = State()
    max_price = State()
    departure_date_custom = State()
    photo_custom = State()

    choice_history = State()
    choice_city_history = State()

    quiz = State()
