# Инструкция Telegram бота.

---
## 1. Содержание 
* #### Как запустить бота.
* #### Экскурс по файлам и папка.
* #### Зависимости
* #### Краткая инструкция по командам бота.

## 2. Как запустить бота.

- Создайте файл '.env'. (Пример того, что деолжен содержать файл есть в файле `.env.template`
   * Вставьте свой [BOT_TOKEN](https://helpdesk.bitrix24.ru/open/17538378/#:~:text=%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D1%83%D1%8E%D1%89%D0%B5%D0%B3%D0%BE%20%D0%B1%D0%BE%D1%82%D0%B0,%D0%B0%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%BD%D0%B5%D0%B3%D0%BE%20%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%20%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9.) и [RAPID_API_KEY](https://rapidapi.com/apidojo/api/hotels4/)


- Создайте виртуальное окружение и загрузите необходимые зависимости из файла `requirements.txt`. Можно сделать это вписав в консоли `pip install -r requirements.txt` 

---
## 3. Экскурс по файлам и папкам.

##### 1. API_site - Инструменты для работы с API hotels.com
* `site_api_handler.py` - инструменты для отправки запросов.
* `Useful_funcs` - инструменты для обработки respons.
* `core` - Ядро папки API_site, где все собирается

##### 2. config_data - Конфигурации.
##### 3. database - Инструменты для работы с базой данных.
* `common` - инструменты для создания базы данных
* `Utils` - инструменты для получения и обработки данных из базы данных
##### 4. handlers - Команды бота
##### 5. keyboards - Инструменты для создания кнопок.
##### 6. states - Состояния пользователя.
##### 7. Utils - Инструменты для передачи списка команд боту.

---
##### 1.Quiz.db - База данных для викторины
##### 2.setup.cfg - Настройки для flake8
##### 3.loader.py - Подгружает конфигурации в бота
##### 4.main.py - Запуск бота 

---
## 4. Зависимости.
  * #### backoff<br>
``Используется для стратегии backoff. Чтобы при неудачном запросе отправлять запрос снова, до тех пор пок запрос не будет удачным``
  * #### flake8<br>
``Линтер для чистоты кода``
  * #### googletrans<br>
``Переводчик``
  * #### loguru<br>
``Используется для логирования``
  * #### peewee<br>
``Работы с базой данных``
  * #### pydantic<br>
``Библиотека для сокрытия чуствительных данных``
  * #### mypy<br>
``Проверка аннотаций``
  * #### pyTelegramBotAPI<br>
``Библиотека для работы с API Telegram``
  * #### requests<br>
``Библиотека для работы с API сайта Rapidapi.com``
  * #### telebot-calendar<br>
``Библиотека для создания Календаря в виде клавиатуры в Telegram``

---
## 5. Краткая инструкция по командам бота.
  * #### start - начало диалога с ботом. 
  * #### custom - Кастомный поиск отелей по вашим ценовым параметрам.
  * #### low - Поиск отелей с минимальной стоимостью в выбранном городе.
  * #### high - Поиск отелей с максимальной стоимостью в выбранном городе.
  * #### echo - Эхо хендлер. Куда попадают сообщения без состояния пользователя
  * #### help - Показывает все доступные и команды.
  * #### history - Хранит историю поисков и показывает последние 10 запросов.
  * #### quiz - Викторина Угадай столицу.