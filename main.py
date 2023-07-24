import telebot
import sqlite3
from telebot import types
from tokennn import token

bot = telebot.TeleBot(token)

serv = {'массаж': 500, 'коллагенарий':2000, 'кедровая бочка':1000, 'спа-капсула':3000}


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute("""
create table if not exists USERS (
            name text,
            lastname text,
            service text,
            price integer,
            date text
            
)
            """)
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Добрый день! Начинаем регистрацию... Введите пожалуйста ваше имя')
    bot.register_next_step_handler(message,first_name)
def first_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пожалуйста вашу фамилию')
    bot.register_next_step_handler(message,last_name)

def last_name(message):
    lastn = message.text.strip()
    # bot.send_message(message.chat.id, '')
    # bot.register_next_step_handler(message,services)
    services(message)

def services(message):
    markup = types.InlineKeyboardMarkup()
    for service,price in serv.items():
        btn = types.InlineKeyboardButton(f'{service} - {price} руб.', callback_data='service')
        markup.row(btn)
    bot.send_message(message.chat.id, 'Выберите процедуры, которые желаете посетить:', reply_markup=markup)
    bot.register_next_step_handler(message, process_service)
    
@bot.callback_query_handler(func=lambda message: True)
def process_service(message):
    pass
    

bot.polling(none_stop = True)


