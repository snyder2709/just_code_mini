from telebot import types
import json
import telebot
import wikipediaapi
from dotenv import load_dotenv
import os
load_dotenv()


token = os.getenv('BOT_API_KEY')
data = None


with open('mock.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

GENRE = {"action": ['экшон нереальный', data['action']],
         'fantastic': ['фантастика', data['fantastic']], "scary": ['ужасы', data['scary']]}


def normalize_data(data):
    messages = []
    for film in data:
        title = film['title']
        year = film['year']
        director = film['director']
        message = f"""Фильм: <strong>{
            title}</strong> \n Год: {year} \n Режиссер: {director}"""
        messages.append(message)
    return '\n'.join(messages)


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")


@bot.message_handler(commands=['wiki'])
def wiki_message(message):
    bot.send_message(message.chat.id, "че надо")
    bot.register_next_step_handler(message, search_req)


@bot.message_handler(commands=['menu'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text="Фантастика")
    item2 = types.KeyboardButton(text="Ужасы")
    item3 = types.KeyboardButton(text="Экшон нереальный")
    markup.add(item1, item2, item3)
    bot.send_message(
        message.chat.id, 'Выберите что вам интересно 😊', reply_markup=markup)


def search_req(message):
    wiki = wikipediaapi.Wikipedia('ilya merlin@example.com', 'ru')
    page_py = wiki.page(message.text)
    bot.send_message(message.chat.id, "щас ищем")
    bot.send_message(
        message.chat.id, page_py.summary[0:300]+'\n Ссылка на статью' + page_py.fullurl)


@bot.message_handler(content_types='text')
def text_handler(message):
    if message.text.lower() == GENRE['action'][0]:
        bot.send_message(message.chat.id, normalize_data(
            GENRE['action'][1]), parse_mode='HTML')
    elif message.text.lower() == GENRE['scary'][0]:
        bot.send_message(message.chat.id, normalize_data(
            GENRE['scary'][1]), parse_mode='HTML')
    elif message.text.lower() == GENRE['fantastic'][0]:
        bot.send_message(message.chat.id,  normalize_data(
            GENRE['action'][1]), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "неть 🤷‍♂️")


bot.infinity_polling()
