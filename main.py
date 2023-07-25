import telebot
import sqlite3
from telebot import types
from tokennn import token

bot = telebot.TeleBot(token)
# massage = 'массаж: 500'
# spa = 'спа-капсула: 3000'
# kolagen = 'коллагенарий: 2000'
serv = {'массаж': 500, 'коллагенарий':2000, 'кедровая бочка':1000, 'спа-капсула':3000}
massage = list(serv)[0]
m_pr = serv[massage]
kolagen = list(serv)[1]
kol_pr = serv[kolagen]
kedr = list(serv)[2]
kedr_pr = serv[kedr]
spa = list(serv)[3]
spa_pr = serv[spa]

selected_serv = {}
key = None
value = None
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
    button(message)
@bot.message_handler(commands=['button'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(f'{massage} - {m_pr}',callback_data=massage)
    btn2 = types.InlineKeyboardButton(f'{kolagen} - {kol_pr}',callback_data=kolagen)
    btn3 = types.InlineKeyboardButton(f'{kedr} - {kedr_pr}',callback_data=kedr)
    btn4 = types.InlineKeyboardButton(f'{spa} - {spa_pr}',callback_data=spa)
    markup.add(btn1,btn2,btn3,btn4)
    bot.send_message(message.chat.id, 'Выберите процедуры, которые желаете посетить:', reply_markup=markup)
    # bot.register_next_step_handler(message, confirm_services)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == massage:
            selected_serv.setdefault(massage,m_pr)
        if call.data == kolagen:
            selected_serv.setdefault(kolagen,kol_pr)
        if call.data == kedr:
            selected_serv.setdefault(kedr,kedr_pr)
        if call.data == spa:
            selected_serv.setdefault(spa,spa_pr)
            
    selected_services = ''        
    for key,value in selected_serv.items():
        selected_services += ''.join(f'{key} - {value}') + ', '
    bot.send_message(call.message.chat.id, f'Вы выбрали: {selected_services[:-2]}')
    



    

bot.polling(none_stop = True)


