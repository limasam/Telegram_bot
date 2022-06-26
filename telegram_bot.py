import requests
import telebot
import random
from telebot import types
from bs4 import BeautifulSoup as BS  # для доступа к информации с веб-страниц
import sqlite3  # импорт базы данных
import config  # импорт config.py

bot = telebot.TeleBot(config.token)  # передаем токен из файла config.py

# указание начальных ссылок для дальнейшего использования
URL = 'https://horoscopes.rambler.ru/'
URL_weather = 'https://weather.rambler.ru/v-'
URL_films = 'https://www.kinoafisha.info/rating/movies/'
URL_tv ='https://tv.belta.by/program-ru/channel/'


# Работа с командой /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создадим базу данных с пользователями
    conn = sqlite3.connect('users.db')
    # Создаем объект cursor, который позволяет нам взаимодействовать с базой данных
    cursor = conn.cursor()
    # Создадим таблицу 'personal_id', в которой будут храниться пользователи (поле id)
    cursor.execute('''CREATE TABLE IF NOT EXISTS personal_id(id INTEGER)''')
    # Сохраняем изменения
    conn.commit()

    # Проверка id на наличие в БД
    people_id = message.chat.id
    cursor.execute(f'''SELECT id FROM personal_id WHERE id = {people_id}''')
    # Если такого id еще нет, то переменная data будет равна 0
    data = cursor.fetchall()
    # Если такого id нету, то оно будет добавляться в БД
    if data is None:
        # Добавляем данные в таблицу
        user_id = [message.chat.id]
        cursor.execute('''INSERT INTO personal_id VALUES(?)''', user_id)
        conn.commit()
    else:
        pass


    # Создание встроенной в сообщение в клавитауры
    markup = types.InlineKeyboardMarkup(row_width=1)  # Количестко кнопок в строке = 1
    # Создание кнопок для клавитуры
    button_1 = types.InlineKeyboardButton('✨Гороскоп на сегодня', callback_data='function_1')
    button_2 = types.InlineKeyboardButton('🌥Погода на сегодня', callback_data='function_2')
    button_3 = types.InlineKeyboardButton('🎬Фильмы по жанрам', callback_data='function_3')
    button_4 = types.InlineKeyboardButton('🦋Что сейчас на тв', callback_data='function_4')
    # Добавление кнопок в клавитуру
    markup.add(button_1, button_2, button_3, button_4)

    # Бот отправляет данное сообщение на команду и прикрепляет клавиатуру
    bot.send_message(message.chat.id, "Приветик. Что тебя интересует?", reply_markup=markup)



# Запускаем обработку кнопок при помощи декоратора
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        # Обрабатываем кнопку гороскопа
        if call.data == 'function_1':  # Если вызывается кнопка 1, то...p
            # Создаем клавиатуру
            markup_horoscope = types.InlineKeyboardMarkup(row_width=1)
            # Создаем кнопки и добавляем их в клавиатуру
            button_aries = types.InlineKeyboardButton('♈ Овен ♈', callback_data='aries')
            markup_horoscope.add(button_aries)
            button_taurus = types.InlineKeyboardButton('♉ Телец ♉', callback_data='taurus')
            markup_horoscope.add(button_taurus)
            button_gemini = types.InlineKeyboardButton('♊ Близнецы ♊', callback_data='gemini')
            markup_horoscope.add(button_gemini)
            button_cancer = types.InlineKeyboardButton('♋ Рак ♋', callback_data='cancer')
            markup_horoscope.add(button_cancer)
            button_leo = types.InlineKeyboardButton('♌ Лев ♌', callback_data='leo')
            markup_horoscope.add(button_leo)
            button_virgo = types.InlineKeyboardButton('♍ Дева ♍', callback_data='virgo')
            markup_horoscope.add(button_virgo)
            button_libra = types.InlineKeyboardButton('♎ Весы ♎', callback_data='libra')
            markup_horoscope.add(button_libra)
            button_scorpio = types.InlineKeyboardButton('♏ Скорпион ♏', callback_data='scorpio')
            markup_horoscope.add(button_scorpio)
            button_saggitarius = types.InlineKeyboardButton('♐ Стрелец ♐', callback_data='sagittarius')
            markup_horoscope.add(button_saggitarius)
            button_capricorn = types.InlineKeyboardButton('♑ Козерог ♑', callback_data='capricorn')
            markup_horoscope.add(button_capricorn)
            button_aquarius = types.InlineKeyboardButton('♒ Водолей ♒', callback_data='aquarius')
            markup_horoscope.add(button_aquarius)
            button_pisces = types.InlineKeyboardButton('♓ Рыбы ♓', callback_data='pisces')
            markup_horoscope.add(button_pisces)
            # Прикрепляем клавиатуру к сообщению с помощью reply_markup
            bot.send_message(call.message.chat.id, 'Какой у тебя знак зодиака?', reply_markup=markup_horoscope)

        # Задаем обработки кнопок гороскопа
        # Обработка кнопки 'Овен'
        if call.data == 'aries':
            # Создаем запрос по ссылке URL для данного знака зодиака
            url_aries = requests.get(URL + 'aries/')
            # Создаем парсер
            soup = BS(url_aries.text, 'html.parser')
            # Ищем нужную информацию по определенному тегу и классу
            horoscope_aries = soup.find_all('p', class_='mtZOt')
            # Создаем список, который перебирает информацию и убирает оттуда теги, оставляя только текст
            list_aries = [i.text for i in horoscope_aries]
            print(list_aries)
            bot.send_message(call.message.chat.id, list_aries)

            # Добавляем кнопку, которая будет возвращать в начало
            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)


        # Обработка кнопки 'Телец'
        elif call.data == 'taurus':
            url_taurus = requests.get(URL + 'taurus/')
            soup = BS(url_taurus.text, 'html.parser')
            horoscope_taurus = soup.find_all('p', class_='mtZOt')
            list_taurus = [i.text for i in horoscope_taurus]
            print(list_taurus)
            bot.send_message(call.message.chat.id, list_taurus)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Близнецы'
        elif call.data == 'gemini':
            url_gemini = requests.get(URL + 'gemini/')
            soup = BS(url_gemini.text, 'html.parser')
            horoscope_gemini = soup.find_all('p', class_='mtZOt')
            list_gemini = [i.text for i in horoscope_gemini]
            print(list_gemini)
            bot.send_message(call.message.chat.id, list_gemini)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Рак'
        elif call.data == 'cancer':
            url_cancer = requests.get(URL + 'cancer/')
            soup = BS(url_cancer.text, 'html.parser')
            horoscope_cancer = soup.find_all('p', class_='mtZOt')
            list_cancer = [i.text for i in horoscope_cancer]
            print(list_cancer)
            bot.send_message(call.message.chat.id, list_cancer)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)




        # Обработка кнопки 'Лев'
        elif call.data == 'leo':
            url_leo = requests.get(URL + 'leo/')
            soup = BS(url_leo.text, 'html.parser')
            horoscope_leo = soup.find_all('p', class_='mtZOt')
            list_leo = [i.text for i in horoscope_leo]
            print(list_leo)
            bot.send_message(call.message.chat.id, list_leo)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Весы'
        elif call.data == 'libra':
            url_libra = requests.get(URL + 'libra/')
            soup = BS(url_libra.text, 'html.parser')
            horoscope_libra = soup.find_all('p', class_='mtZOt')
            list_libra = [i.text for i in horoscope_libra]
            print(list_libra)
            bot.send_message(call.message.chat.id, list_libra)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Скорпион'
        elif call.data == 'scorpio':
            url_scorpio = requests.get(URL + 'scorpio/')
            soup = BS(url_scorpio.text, 'html.parser')
            horoscope_scorpio = soup.find_all('p', class_='mtZOt')
            list_scorpio = [i.text for i in horoscope_scorpio]
            print(list_scorpio)
            bot.send_message(call.message.chat.id, list_scorpio)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)




        # Обработка кнопки 'Стрелец'
        elif call.data == 'sagittarius':
            url_sagittarius = requests.get(URL + 'sagittarius/')
            soup = BS(url_sagittarius.text, 'html.parser')
            horoscope_sagittarius = soup.find_all('p', class_='mtZOt')
            list_sagittarius = [i.text for i in horoscope_sagittarius]
            print(list_sagittarius)
            bot.send_message(call.message.chat.id, list_sagittarius)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Козерог'
        elif call.data == 'capricorn':
            url_capricorn = requests.get(URL + 'capricorn/')
            soup = BS(url_capricorn.text, 'html.parser')
            horoscope_capricorn = soup.find_all('p', class_='mtZOt')
            list_capricorn = [i.text for i in horoscope_capricorn]
            print(list_capricorn)
            bot.send_message(call.message.chat.id, list_capricorn)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Водолей'
        elif call.data == 'aquarius':
            url_aquarius = requests.get(URL + 'aquarius/')
            soup = BS(url_aquarius.text, 'html.parser')
            horoscope_aquarius = soup.find_all('p', class_='mtZOt')
            list_aquarius = [i.text for i in horoscope_aquarius]
            print(list_aquarius)
            bot.send_message(call.message.chat.id, list_aquarius)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)




        # Обработка кнопки 'Рыбы'
        elif call.data == 'pisces':
            url_pisces = requests.get(URL + 'pisces/')
            soup = BS(url_pisces.text, 'html.parser')
            horoscope_pisces = soup.find_all('p', class_='mtZOt')
            list_pisces = [i.text for i in horoscope_pisces]
            print(list_pisces)
            bot.send_message(call.message.chat.id, list_pisces)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Погода на сегодня'
        if call.data == 'function_2':
            # Создаем клавиатуру
            markup_weather = types.InlineKeyboardMarkup(row_width=1)
            # Создаем кнопки и добавляем их в клавиатуру
            button_grodno = types.InlineKeyboardButton('Гродно 🌿', callback_data='grodno')
            markup_weather.add(button_grodno)
            button_brest = types.InlineKeyboardButton('Брест 🌱', callback_data='brest')
            markup_weather.add(button_brest)
            button_minsk = types.InlineKeyboardButton('Минск 🌾', callback_data='minsk')
            markup_weather.add(button_minsk)
            button_vitebsk = types.InlineKeyboardButton('Витебск 🍃', callback_data='vitebsk')
            markup_weather.add(button_vitebsk)
            button_mogilev = types.InlineKeyboardButton('Могилев ☘', callback_data='mogilev')
            markup_weather.add(button_mogilev)
            button_gomel = types.InlineKeyboardButton('Гомель 🍂', callback_data='gomel')
            markup_weather.add(button_gomel)

            bot.send_message(call.message.chat.id, 'Выбери свой город', reply_markup=markup_weather)



        # Задаем обработки кнопок погоды
        # Обработка кнопки 'Гродно'
        if call.data == 'grodno':
            url_grodno = requests.get(URL_weather + 'grodno/today/')
            soup = BS(url_grodno.text, 'html.parser')
            weather_grodno = soup.find_all('p', class_='_3xiF')
            list_grodno = [i.text for i in weather_grodno]
            print(list_grodno)
            bot.send_message(call.message.chat.id, list_grodno)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Брест'
        elif call.data == 'brest':
            url_brest = requests.get(URL_weather + 'breste/today/')
            soup = BS(url_brest.text, 'html.parser')
            weather_brest = soup.find_all('p', class_='_3xiF')
            list_brest = [i.text for i in weather_brest]
            print(list_brest)
            bot.send_message(call.message.chat.id, list_brest)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Минск'
        elif call.data == 'minsk':
            url_minsk = requests.get(URL_weather + 'minske/today/')
            soup = BS(url_minsk.text, 'html.parser')
            weather_minsk = soup.find_all('p', class_='_3xiF')
            list_minsk = [i.text for i in weather_minsk]
            print(list_minsk)
            bot.send_message(call.message.chat.id, list_minsk)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Витебск'
        elif call.data == 'vitebsk':
            url_vitebsk = requests.get(URL_weather + 'vitebske/today/')
            soup = BS(url_vitebsk.text, 'html.parser')
            weather_vitebsk = soup.find_all('p', class_='_3xiF')
            list_vitebsk = [i.text for i in weather_vitebsk]
            print(list_vitebsk)
            bot.send_message(call.message.chat.id, list_vitebsk)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Могилев'
        elif call.data == 'mogilev':
            url_mogilev = requests.get(URL_weather + 'mogilyove/today/')
            soup = BS(url_mogilev.text, 'html.parser')
            weather_mogilev = soup.find_all('p', class_='_3xiF')
            list_mogilev = [i.text for i in weather_mogilev]
            print(list_mogilev)
            bot.send_message(call.message.chat.id, list_mogilev)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)


        # Обработка кнопки 'Гомель'
        elif call.data == 'gomel':
            url_gomel = requests.get(URL_weather + 'gomele/today/')
            soup = BS(url_gomel.text, 'html.parser')
            weather_gomel = soup.find_all('p', class_='_3xiF')
            list_gomel = [i.text for i in weather_gomel]
            print(list_gomel)
            bot.send_message(call.message.chat.id, list_gomel)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Фильмы по жанрам'
        if call.data == 'function_3':
            markup_films = types.InlineKeyboardMarkup(row_width=1)
            button_anime = types.InlineKeyboardButton('📌 Аниме', callback_data='anime')
            markup_films.add(button_anime)
            button_action = types.InlineKeyboardButton('📌 Боевики', callback_data='action')
            markup_films.add(button_action)
            button_mystery = types.InlineKeyboardButton('📌 Детективы', callback_data='mystery')
            markup_films.add(button_mystery)
            button_drama = types.InlineKeyboardButton('📌 Драма', callback_data='drama')
            markup_films.add(button_drama)
            button_comedy = types.InlineKeyboardButton('📌 Комедия', callback_data='comedy')
            markup_films.add(button_comedy)
            button_romance = types.InlineKeyboardButton('📌 Мелодрама', callback_data='romance')
            markup_films.add(button_romance)
            button_animation = types.InlineKeyboardButton('📌 Мультфильмы', callback_data='animation')
            markup_films.add(button_animation)
            button_adventure = types.InlineKeyboardButton('📌 Приключения', callback_data='adventure')
            markup_films.add(button_adventure)
            button_family = types.InlineKeyboardButton('📌 Семейные', callback_data='family')
            markup_films.add(button_family)
            button_thriller = types.InlineKeyboardButton('📌 Триллеры', callback_data='thriller')
            markup_films.add(button_thriller)
            button_horror = types.InlineKeyboardButton('📌 Ужасы', callback_data='horror')
            markup_films.add(button_horror)
            button_fantasy = types.InlineKeyboardButton('📌 Фантастика', callback_data='fantasy')
            markup_films.add(button_fantasy)

            bot.send_message(call.message.chat.id, '📽 Какой жанр кино тебя интересует?', reply_markup=markup_films)



        # Задаем обработки кнопок фильмов
        # Обработка кнопки 'Аниме'
        if call.data == 'anime':
            url_anime = requests.get(URL_films + 'anime/')
            soup = BS(url_anime.text, 'html.parser')
            anime_films = soup.find_all('a', class_='movieItem_title')
            # Перемешиваем названия всех фильмов
            random.shuffle(anime_films)
            # Создаем цикл for, чтобы перебрать фильмы и по итогу вывести не все, а только 10
            for film in anime_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if anime_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Боевик'
        elif call.data == 'action':
            url_action = requests.get(URL_films + 'action/')
            soup = BS(url_action.text, 'html.parser')
            action_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(action_films)
            for film in action_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if action_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Детективы'
        elif call.data == 'mystery':
            url_mystery = requests.get(URL_films + 'mystery/')
            soup = BS(url_mystery.text, 'html.parser')
            mystery_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(mystery_films)
            for film in mystery_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if mystery_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Драма'
        elif call.data == 'drama':
            url_drama = requests.get(URL_films + 'drama/')
            soup = BS(url_drama.text, 'html.parser')
            drama_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(drama_films)
            for film in drama_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if drama_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Комедии'
        elif call.data == 'comedy':
            url_comedy = requests.get(URL_films + 'comedy/')
            soup = BS(url_comedy.text, 'html.parser')
            comedy_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(comedy_films)
            for film in comedy_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if comedy_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Мелодрама'
        elif call.data == 'romance':
            url_romance = requests.get(URL_films + 'romance/')
            soup = BS(url_romance.text, 'html.parser')
            romance_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(romance_films)
            for film in romance_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if romance_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Мультфильмы'
        elif call.data == 'animation':
            url_animation = requests.get(URL_films + 'animation/')
            soup = BS(url_animation.text, 'html.parser')
            animation_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(animation_films)
            for film in animation_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if animation_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Приключения'
        elif call.data == 'adventure':
            url_adventure = requests.get(URL_films + 'adventure/')
            soup = BS(url_adventure.text, 'html.parser')
            adventure_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(adventure_films)
            for film in adventure_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if adventure_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Семейные'
        elif call.data == 'family':
            url_family = requests.get(URL_films + 'family/')
            soup = BS(url_family.text, 'html.parser')
            family_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(family_films)
            for film in family_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if family_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Триллер'
        elif call.data == 'thriller':
            url_thriller = requests.get(URL_films + 'thriller/')
            soup = BS(url_thriller.text, 'html.parser')
            thriller_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(thriller_films)
            for film in thriller_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if thriller_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Ужасы'
        elif call.data == 'horror':
            url_horror = requests.get(URL_films + 'horror/')
            soup = BS(url_horror.text, 'html.parser')
            horror_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(horror_films)
            for film in horror_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if horror_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Фантастика'
        elif call.data == 'fantasy':
            url_fantasy = requests.get(URL_films + 'fantasy/')
            soup = BS(url_fantasy.text, 'html.parser')
            fantasy_films = soup.find_all('a', class_='movieItem_title')
            random.shuffle(fantasy_films)
            for film in fantasy_films:
                print(film.text)
                bot.send_message(call.message.chat.id, film.text)
                if fantasy_films.index(film) == 9:
                    break

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки программ на ТВ
        if call.data == 'function_4':
            # Создание клавиатуры
            markup_tv = types.InlineKeyboardMarkup(row_width=1)
            # Создание и добавление кнопок
            button_belarus1 = types.InlineKeyboardButton('Беларусь 1', callback_data='belarus_1')
            markup_tv.add(button_belarus1)
            button_belarus_2 = types.InlineKeyboardButton('Беларусь 2', callback_data='belarus_2')
            markup_tv.add(button_belarus_2)
            button_belarus_5 = types.InlineKeyboardButton('ВТВ', callback_data='vtv')
            markup_tv.add(button_belarus_5)
            button_tv3 = types.InlineKeyboardButton('ТВ3 - МИНСК', callback_data='tv3')
            markup_tv.add(button_tv3)
            button_animal_planet = types.InlineKeyboardButton('ANIMAL PLANET EUROPE', callback_data='animal_planet')
            markup_tv.add(button_animal_planet)
            button_tv1000 = types.InlineKeyboardButton('TV1000', callback_data='tv1000')
            markup_tv.add(button_tv1000)
            button_viasat_history = types.InlineKeyboardButton('VIASAT HISTORY', callback_data='viasat_history')
            markup_tv.add(button_viasat_history)
            button_children = types.InlineKeyboardButton('ДЕТСКИЙ МИР', callback_data='children')
            markup_tv.add(button_children)
            button_nickelodeon = types.InlineKeyboardButton('NICKELODEON', callback_data='nickelodeon')
            markup_tv.add(button_nickelodeon)

            bot.send_message(call.message.chat.id, "Про какой канал хотите узнать?", reply_markup=markup_tv)



        # Обработка кнопки 'Беларусь 1'
        if call.data == 'belarus_1':
            url_tv = requests.get(URL_tv + '140/')
            soup = BS(url_tv.text, 'html.parser')
            time_belarus_1 = soup.find_all('div', class_='tv_chanel_date')
            pr_belarus1 = soup.find_all('div', class_='tv_chanel_title')
            list_belarus1 = [i.text for i in pr_belarus1]  # Название передачи
            list_time = [i.text for i in time_belarus_1]  # Время передачи
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_belarus1)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Беларусь 2'
        elif call.data == 'belarus_2':
            url_tv = requests.get(URL_tv + '86/')
            soup = BS(url_tv.text, 'html.parser')
            time_belarus_2 = soup.find_all('div', class_='tv_chanel_date')
            pr_belarus2 = soup.find_all('div', class_='tv_chanel_title')
            list_belarus2 = [i.text for i in pr_belarus2]
            list_time = [i.text for i in time_belarus_2]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_belarus2)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'ВТВ'
        elif call.data == 'vtv':
            url_tv = requests.get(URL_tv + '95/')
            soup = BS(url_tv.text, 'html.parser')
            time_vtv = soup.find_all('div', class_='tv_chanel_date')
            pr_vtv = soup.find_all('div', class_='tv_chanel_title')
            list_vtv = [i.text for i in pr_vtv]
            list_time = [i.text for i in time_vtv]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_vtv)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'ТВ3 МИНСК'
        elif call.data == 'tv3':
            url_tv = requests.get(URL_tv + '45/')
            soup = BS(url_tv.text, 'html.parser')
            time_tv3 = soup.find_all('div', class_='tv_chanel_date')
            pr_tv3 = soup.find_all('div', class_='tv_chanel_title')
            list_tv3 = [i.text for i in pr_tv3]
            list_time = [i.text for i in time_tv3]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_tv3)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)


        # Обработка кнопки 'animal_planet'
        elif call.data == 'animal_planet':
            url_tv = requests.get(URL_tv + '19/')
            soup = BS(url_tv.text, 'html.parser')
            time_ap = soup.find_all('div', class_='tv_chanel_date')
            pr_ap = soup.find_all('div', class_='tv_chanel_title')
            list_ap = [i.text for i in pr_ap]
            list_time = [i.text for i in time_ap]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_ap)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'tv1000'
        elif call.data == 'tv1000':
            url_tv = requests.get(URL_tv + '103/')
            soup = BS(url_tv.text, 'html.parser')
            time_tv1000 = soup.find_all('div', class_='tv_chanel_date')
            pr_tv1000 = soup.find_all('div', class_='tv_chanel_title')
            list_tv1000 = [i.text for i in pr_tv1000]
            list_time = [i.text for i in time_tv1000]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_tv1000)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'viasat_history'
        elif call.data == 'viasat_history':
            url_tv = requests.get(URL_tv + '106/')
            soup = BS(url_tv.text, 'html.parser')
            time_vh = soup.find_all('div', class_='tv_chanel_date')
            pr_vh = soup.find_all('div', class_='tv_chanel_title')
            list_vh = [i.text for i in pr_vh]
            list_time = [i.text for i in time_vh]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_vh)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'Детский мир'
        elif call.data == 'children':
            url_tv = requests.get(URL_tv + '130/')
            soup = BS(url_tv.text, 'html.parser')
            time_children = soup.find_all('div', class_='tv_chanel_date')
            pr_children = soup.find_all('div', class_='tv_chanel_title')
            list_children = [i.text for i in pr_children]
            list_time = [i.text for i in time_children]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_children)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)



        # Обработка кнопки 'nickelodeon'
        elif call.data == 'nickelodeon':
            url_tv = requests.get(URL_tv + '74/')
            soup = BS(url_tv.text, 'html.parser')
            time_nickelodeon = soup.find_all('div', class_='tv_chanel_date')
            pr_nickelodeon = soup.find_all('div', class_='tv_chanel_title')
            list_nickelodeon = [i.text for i in pr_nickelodeon]
            list_time = [i.text for i in time_nickelodeon]
            bot.send_message(call.message.chat.id, list_time)
            bot.send_message(call.message.chat.id, list_nickelodeon)

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton('➡ Вернуться в начало ⬅', callback_data='function_back')
            markup_back.add(button_back)
            bot.send_message(call.message.chat.id, "📍Нажмите, чтобы вернуться в начало📍", reply_markup=markup_back)


        # Обработка кнопки 'Вернуться назад'
        if call.data == 'function_back':
            markup = types.InlineKeyboardMarkup(row_width=1)  # Количестко кнопок в строке = 1
            button_1 = types.InlineKeyboardButton('✨Гороскоп на сегодня', callback_data='function_1')
            button_2 = types.InlineKeyboardButton('🌥Погода на сегодня', callback_data='function_2')
            button_3 = types.InlineKeyboardButton('🎬Фильмы по жанрам', callback_data='function_3')
            button_4 = types.InlineKeyboardButton('🦋Что сейчас на тв', callback_data='function_4')
            markup.add(button_1, button_2, button_3, button_4)

            bot.send_message(call.message.chat.id, "Хотите еще что-нибудь узнать?", reply_markup=markup)


# Работа с командой /delete
# Удаляет id из базы данных
@bot.message_handler(commands=['delete'])
def delete(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    people_id = message.chat.id
    cursor.execute(f'''DELETE FROM personal_id WHERE id = {people_id}''')
    conn.commit()


# Работа с командами /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Выполни команду /start, чтобы узнать мои возможности")


# Работа с текстовыми сообщеняими
@bot.message_handler(content_types=['text'])
def bla_bla_bla(message):
    bot.send_message(message.chat.id, "К сожалению, на данный момент мой создатель еще не одарил меня навыками "
                                      "общения, но думаю, что в скором времени он это исправит и мы обязательно"
                                      " с тобой поболтаем 🙃")


# Обработка ошибки запуска бота
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except ConnectionError as c:
        print('Ошибка соединения', c)
    except Exception as e:
        print('Непредвиденная ошибка', e)
    finally:
        print('Здесь все закончилось')