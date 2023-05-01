import telebot
from telebot import types
import requests
import json
import re

token = '6189988882:AAGpiRgHErwH3KMUdQdcS718mMVV9EgfNGg'

bot = telebot.TeleBot(token)

answers = {}

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.reply_to(message, 'Привет, я бот! Что ты хочешь сделать?')
  
  bot.send_message(message.chat.id, "Введите ваше ФИО:")
  bot.register_next_step_handler(message, get_fullname)

def get_fullname(message):
    # Сохраняем ФИО и запрашиваем у пользователя номер телефона
    fullname = message.text
    # Проверка маски в поле "ФИО"
    if not re.match(r"^[a-zA-Zа-яА-Я ]+$", fullname):
        bot.reply_to(message, "Некорректное ФИО, пожалуйста, введите еще раз:")
        bot.register_next_step_handler(message, get_fullname)
        return
    answers["name"] = fullname
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(message, get_phone_number, fullname)

def get_phone_number(message, fullname):
    # Сохраняем номер телефона и подтверждаем получение заявки
    phone_number = message.text
    # Проверка маски в поле "Номер телефона"
    if not re.match(r"^[0-9]+$", phone_number):
        bot.reply_to(message, "Некорректный номер телефона, пожалуйста, введите еще раз:")
        bot.register_next_step_handler(message, get_phone_number, fullname)
        return
    answers["phone"] = phone_number

    print(json.dumps(answers))

    # отправка ответов на сайт
    data = {'name': answers['name'], 'phone': answers['phone']}
    response = requests.post('https://platforma.bz/api2/tg/', data=data)

    if response.status_code == 200:
        bot.send_message(message.chat.id, f"Спасибо, вы отправили заявку! ФИО: {fullname}, номер телефона: {phone_number}")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка при отправке заявки, попробуйте еще раз")



# print(json.dumps(answers))
bot.polling(none_stop=True)