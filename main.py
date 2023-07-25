import telebot
import sqlite3
from telebot import types
from tokennn import token
from datetime import datetime,timedelta

bot = telebot.TeleBot(token)

# услуги
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
date = None
time = None
records = {}
record = {}
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
            date text,
            time text
            
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
    bot.send_message(call.message.chat.id, f'Вы выбрали: {selected_services[:-2]}. Чтобы выбрать дату и время введите /запись либо добавьте еще услуги')
    # bot.register_next_step_handler(call,handle_booking)

# удалить
@bot.message_handler(commands=['запись'])
def handle_booking(message):
    chat_id = message.chat.id
    # создаем клавиатуру с выбором даты
    markup = create_date_keyboard()
    bot.send_message(chat_id, 'Укажите дату записи (в формате ДД.ММ.ГГГГ):', reply_markup=markup)

# обработка ответа с выбранной датой
@bot.message_handler(func=lambda message: True if message.text.count('.') == 2 else False)
def handle_date(message):
    chat_id = message.chat.id
    date_str = message.text

    try:
        # преобразуем строку с датой в объект datetime
        date = datetime.strptime(date_str, '%d.%m.%Y')
        # создаем клавиатуру с выбором времени
        markup = create_time_keyboard()
        bot.send_message(chat_id, 'Укажите время записи (в формате ЧЧ:ММ):', reply_markup=markup)
        # сохраняем запись в словаре
        records[chat_id] = {'date': date, 'time': None}
    except ValueError:
        bot.send_message(chat_id, 'Неверный формат даты! Попробуйте еще раз.')

# обработка ответа с выбранным временем
@bot.message_handler(func=lambda message: True if ':' in message.text else False)
def handle_time(message):
    chat_id = message.chat.id
    time_str = message.text

    try:
        # преобразуем строку с временем в объект datetime
        time = datetime.strptime(time_str, '%H:%M').time()
        # получаем запись из словаря
        record = records.get(chat_id)
        if record:
            # устанавливаем выбранное время
            record['time'] = time
            bot.send_message(chat_id, 'Вы успешно записаны на {date} в {time}'.format(date=record['date'].strftime('%d.%m.%Y'), time=record['time'].strftime('%H:%M')),reply_markup=None)
            print(record)
    except ValueError:
        bot.send_message(chat_id, 'Неверный формат времени! Попробуйте еще раз.',reply_markup=None)
    
    
# создание клавиатуры с выбором даты
def create_date_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    today = datetime.now().date()
    for i in range(7):
        date = today + timedelta(days=i)
        button_text = date.strftime('%d.%m.%Y')
        markup.add(types.KeyboardButton(button_text))
    return markup

# создание клавиатуры с выбором времени
def create_time_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    for hour in range(8, 21):
        for minute in range(0, 60):
            time = '{:02d}:{:02d}'.format(hour, minute)
            markup.add(types.KeyboardButton(time))
    return markup

    





    

bot.polling(none_stop = True)


