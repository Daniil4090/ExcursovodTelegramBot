import os
import random
import sqlite3
import telebot
from telebot import types
import json

bot = telebot.TeleBot('6296766499:AAEv9zaOjwyqS34pc2tvkjTtHy75WZwquUc')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Привет!")
    markup.add(btn1)
    bot.send_message(message.from_user.id,
                     "Привет я Экскурсовод! Я смогу подсказать тебе парочку интересных мест в городе или сразу вывести "
                     "на твой экран все места.",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Случайное место')
        btn2 = types.KeyboardButton('Вывести все места')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Выберите интересующее вас действие.', reply_markup=markup)
    elif message.text == 'Вывести все места':
        directory = 'Places'
        places = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
        for i in range(places):
            with open(f"Places/{i}.json", encoding="utf-8") as place_file:
                place_info = json.load(place_file)
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='На карте', url=place_info["way_url"])
            markup.add(btn1)
            if place_info["off_site"] != "":
                btn2 = types.InlineKeyboardButton(text='Оффициальный сайт', url=place_info["off_site"])
                markup.add(btn2)
            bot.send_message(message.from_user.id,
                             f'{place_info["place"]}',
                             reply_markup=markup)
    elif message.text == 'Случайное место':
        directory = 'Places'
        places = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
        with open(f"Places/{random.choice(range(places))}.json", encoding="utf-8") as place_file:
            place_info = json.load(place_file)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='На карте', url=place_info["way_url"])
        markup.add(btn1)
        if place_info["off_site"] != "":
            btn2 = types.InlineKeyboardButton(text='Оффициальный сайт', url=place_info["off_site"])
            markup.add(btn2)
        bot.send_message(message.from_user.id,
                         f'{place_info["place"]}\nОписание:\n{place_info["description"]}',
                         reply_markup=markup)
    else:
        places = db_cur.execute(f"""SELECT DISTINCT id FROM Places_id WHERE name LIKE LOWER('%{message.text.lower()}%')""").fetchall()
        for place in places:
            with open(f"Places/{place[0]}.json", encoding="utf-8") as place_file:
                place_info = json.load(place_file)
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='На карте', url=place_info["way_url"])
            markup.add(btn1)
            if place_info["off_site"] != "":
                btn2 = types.InlineKeyboardButton(text='Оффициальный сайт', url=place_info["off_site"])
                markup.add(btn2)
            bot.send_message(message.from_user.id,
                             f'{place_info["place"]}\nОписание:\n{place_info["description"]}',
                             reply_markup=markup)
        if len(places) == 0:
            bot.send_message(message.from_user.id,
                             'Я не знаю такого места.')


db = sqlite3.connect("db/Places.db", check_same_thread=False)
db_cur = db.cursor()
bot.polling(none_stop=True, interval=0)
