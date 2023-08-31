import datetime
import re
from typing import Dict, List

from googletrans import Translator


def abbreviated_names(city_name: str) -> str:
    """ Функция , которая на вход получает получает имя города превыщающее
    допустимое значение символов и сокращает до нужного количества символов."""
    name = city_name[:30].split()
    name = name[0:-1]
    name = ' '.join(name)
    new_name = ''

    if name[-1] == ',':
        name = name[0:-1]

    for elem in name:
        if elem.isalpha() or elem in [' ', ',', '-']:
            new_name += elem

    return new_name


def _find_photo(all_hotels_info: Dict) -> List:
    """ Функция, которая на вход получает словарь с информацие о конкретном отеле,
    находит в словаре все url содержащие различные фото конкретного отеля. Среди всех
    фотографий находит и возращает возвращает url содержащий фото фасада(если оно есть)
    и расстояние до центра города."""

    info_list = list()
    photo_list = all_hotels_info['data']['propertyInfo']['propertyGallery']['images']

    address = all_hotels_info['data']['propertyInfo']['summary']['location']['address']['addressLine']
    info_list.append(address)

    for photo in photo_list:

        text = photo['accessibilityText'].lower()
        result = re.search(r'фасад объекта', text)

        if result:
            info_list.append(photo['image']['url'])
            return info_list

        text = photo['accessibilityText'].lower()
        result = re.search(r'фасад', text)

        if result:
            info_list.append(photo['image']['url'])
            return info_list
    else:

        photo_list = all_hotels_info['data']['propertyInfo']['propertyGallery']['images']
        photo = photo_list[0]['image']['url']
        info_list.append(photo)
        return info_list


def _sorted_info(hotels_list: List, hotels_count: int) -> List:
    """ Функция, которая на вход получает список состоящие из словорей, которые содержат информацию
    о всех отелях, и целое число , которое указывает сколько должно быть отелей в новом списке.
    Вовзращает новый осортированный список который содержит только id, имя отеля, цену
    и расстояние до центра города"""
    sorted_list = list()
    for hotel in hotels_list:
        temporary_list = list()

        hotel_id = hotel['id']
        hotel_name = hotel['name']
        hotel_price = round(hotel['price']['lead']['amount'])
        hotel_destination = hotel['destinationInfo']['distanceFromDestination']['value']

        temporary_list.append(hotel_id)
        temporary_list.append(hotel_name)
        temporary_list.append(hotel_price)
        temporary_list.append(hotel_destination)

        sorted_list.append(temporary_list)
        if len(sorted_list) >= hotels_count:
            break

    return sorted_list


def _cities_dict(cities_list: List) -> Dict:
    """ Функция которая получает на вход список из словарей , которые содержат все совпадение
     по искомому городу. И создает словарь , который содержит название , и id города или района."""
    sorted_cities_dict = dict()
    for city in cities_list:
        if 'gaiaId' in city:
            name = city['regionNames']['fullName']
            if len(name) > 30:
                name = abbreviated_names(name)
            sorted_cities_dict[name] = city['gaiaId']

    return sorted_cities_dict


def _property_sorted(property_info: Dict) -> Dict:
    """ Функция, которая на вход получает словарь, который содержит детальную информацию о конкретном отеле,
    и возвращает новый словарь , который содержит название отеля, фотографии и описания к ним."""
    sorted_info = dict()
    translator = Translator()

    try:
        sorted_info['name'] = property_info['data']['propertyInfo']['summary']['name']
    except (AttributeError, KeyError, TypeError):
        sorted_info['name'] = '-'

    try:
        sorted_info['info'] = property_info['data']['propertyInfo']['summary']['policies']['needToKnow']['body']
    except (AttributeError, KeyError, TypeError):
        sorted_info['info'] = '-'

    try:
        sorted_info['stars'] = property_info['data']['propertyInfo']['summary']['overview']['propertyRating']['rating']
    except (AttributeError, KeyError, TypeError):
        sorted_info['stars'] = '-'

    try:
        sorted_info['rating'] = \
            property_info['data']['propertyInfo']['reviewInfo']['summary']['overallScoreWithDescriptionA11y'][
                'value'].split(
                ' ')
    except (AttributeError, KeyError, TypeError):
        sorted_info['rating'] = '-'

    gallery = property_info['data']['propertyInfo']['propertyGallery']['images']
    sorted_info['images'] = list()

    for image in gallery[:5]:
        temporary_list = list()

        translation = translator.translate(image['image']['description'], dest="ru")

        temporary_list.append(translation.text)
        temporary_list.append(image['image']['url'])

        sorted_info['images'].append(temporary_list)

    return sorted_info


def _date_comparison(date_first: datetime, date_second: datetime) -> bool:
    """ Функция, которая проверяет чтобы дата выезда не была раньше даты заезда"""
    date_first = date_first.split('.')
    date_second = date_second.split('.')

    date_first = list(reversed(date_first))
    date_second = list(reversed(date_second))

    date_first = datetime.datetime(int(date_first[0]), int(date_first[1]), int(date_first[2]))
    date_second = datetime.datetime(int(date_second[0]), int(date_second[1]), int(date_second[2]))

    if date_second > date_first:
        return True

    else:
        return False


def _new_payload(payload: Dict, data: Dict) -> Dict:
    """Функция, которая получает на вход словарь 'payload' и словарь 'data', который содержит все данные введеные
    пользователем. Далее она заменяет значения в 'payload' значениями из словая 'data'"""
    payload['destination']['regionId'] = data['city_id']

    arrival_date = data['arrival_date'].split('.')

    for num in arrival_date:

        if num.startswith('0'):
            index = arrival_date.index(num)
            arrival_date[index] = num[1:]

    arrival_date_dict = dict()
    arrival_date_dict['day'] = int(arrival_date[0])
    arrival_date_dict['month'] = int(arrival_date[1])
    arrival_date_dict['year'] = int(arrival_date[2])
    payload['checkInDate'] = arrival_date_dict

    departure_date = data['departure_date'].split('.')

    for num in departure_date:

        if num.startswith('0'):
            index = departure_date.index(num)
            departure_date[index] = num[1:]

    departure_date_dict = dict()
    departure_date_dict['day'] = int(departure_date[0])
    departure_date_dict['month'] = int(departure_date[1])
    departure_date_dict['year'] = int(departure_date[2])
    payload['checkOutDate'] = departure_date_dict

    payload['rooms'] = [
        {
            "adults": int(data['adults']),
            "children": []
        }
    ]
    if 'max' in data:
        payload['filters'] = {"price": {
            "max": int(data['max']),
            "min": int(data['min'])
        }}

    return payload


class Utils():
    @staticmethod
    def find_photo():
        return _find_photo

    @staticmethod
    def sorted_info():
        return _sorted_info

    @staticmethod
    def cities_dict():
        return _cities_dict

    @staticmethod
    def property_sorted():
        return _property_sorted

    @staticmethod
    def date_comparison():
        return _date_comparison

    @staticmethod
    def new_payload():
        return _new_payload


if __name__ == '__main__':
    _find_photo()
    _sorted_info()
    _cities_dict()
    _property_sorted()
    _date_comparison()
    _new_payload()

    Utils()
