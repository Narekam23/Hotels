from typing import Dict, Tuple

from peewee import Table


def _create_history_dict(database: Table, user_id: int) -> Dict:
    """Функция, которая получает на вход таблицу и id пользователя.
    Находит все строки, в которых сходится id и формирует список.
    Из последних 10 элементов списка формирует словарь.
    (Для дальнейшего удобства вывода истории)"""
    history_dict = dict()
    row_list = list()

    for row in database.select():
        if row.telegram_id == user_id:
            row_list.append(row)

    row_list = row_list[-10:]

    for elem in row_list:
        history_dict[elem.id] = [
            {"region": elem.region},
            {"name": elem.name},
            {"address": elem.address},
            {"destination": elem.destination},
            {"star": elem.star},
            {"rating": elem.rating},
            {"info": elem.info},
            {"photo": elem.photo},
            {"datatime": elem.datatime},
        ]

    return history_dict


def _create_history_text(database_dict: Dict) -> str:
    """Функция которая состовляет текст истории"""
    text = ''
    for value in enumerate(database_dict.values(), start=1):
        for elem in value[1]:
            if "region" in elem:
                text += str(value[0]) + '. '
                text += elem["region"] + ' - '
            if "name" in elem:
                text += elem["name"] + ' - '
            if "datatime" in elem:
                text += elem["datatime"] + '\n'

    return text


def _create_text(database_dict: Dict, number) -> Tuple:
    """Функция которая состовляет текст в истории по конкретному отелю"""
    text = ''
    photo = ''
    for key in database_dict:

        if str(key) == number:
            text += "Регион: "
            text += database_dict[key][0]['region']
            text += "\nНазвание отеля: "
            text += database_dict[key][1]['name']
            text += "\nАдрес: "
            text += database_dict[key][2]['address']
            text += "\nРасстояние до центра города: "
            text += database_dict[key][3]['destination']
            text += "\nКоличество звёзд: "
            text += database_dict[key][4]['star']
            text += "\nРейтинг: "
            text += database_dict[key][5]['rating']
            text += "\nПодробная информация: "
            text += database_dict[key][6]['info']

            photo += database_dict[key][7]['photo']

    return text, photo


class DatabaseUtils():
    @staticmethod
    def create_history_dict():
        return _create_history_dict

    @staticmethod
    def create_history_text():
        return _create_history_text

    @staticmethod
    def create_text():
        return _create_text


if __name__ == '__main__':
    _create_history_dict()
    _create_history_text()
    _create_text()

    DatabaseUtils()
