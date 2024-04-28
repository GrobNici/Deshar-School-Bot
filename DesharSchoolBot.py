import telebot
from telebot import types
import sqlite3 as sql





TOKEN = '5970535905:AAGWQb0JXkEs9FDjPAjRgkz0xJ1RKF56bvA'
bot = telebot.TeleBot(TOKEN)
username = None
firstname = None


def add_user(name, first_name):
    database = sql.connect('users.sqlite')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT,
                        firstname TEXT
                   )''')
    cursor.execute("INSERT INTO users (username, firstname) VALUES (?, ?)", (name, first_name,))
    database.commit()


@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = "Привет! Я бот помощник. Вот список доступных команд:\n" \
                   "/help - Получить список команд\n" \
                   "/start - Начать взаимодействие с ботом\n" \
                   "/info - Получить информацию о боте\n" \
                   "/stop - Остановить взаимодействие с ботом"
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global username
    global firstname
    username = message.from_user.username
    firstname = message.from_user.first_name
    welcome_message = "Здравствуйте! Я бот помощник онлайн-школы английского Deshar School.\n" \
                      "Что вас интересует?"
    markup = types.InlineKeyboardMarkup()
    button_3 = types.InlineKeyboardButton('Пройти курс', callback_data='show_course')
    button_4 = types.InlineKeyboardButton('Учить слова', callback_data='learn_words')
    button_5 = types.InlineKeyboardButton('Тексты на английском', callback_data='english_texts')
    markup.add(button_3, button_4, button_5)
    bot.reply_to(message, welcome_message, reply_markup=markup)


@bot.message_handler(commands=['to_sign_up'])
def to_sign_upToLesson(message):
    markup = types.InlineKeyboardMarkup()
    button_2 = types.InlineKeyboardButton('Оставить контакты', callback_data='sign_up_for_lesson')
    text = 'Чтобы записаться на урок нужно оставить свои контакты.\n' \
           'Для этого нажмите на кнопку "Оставить контакты".'
    markup.add(button_2)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['info'])
def about_us(message):
    text = f'''Привет, {firstname}, мы школа английского Deshar School!
Работаем уже 7 лет, наши преподаватели 15 лет говорят по-английски, аттестованы Кембриджем. Профессиональные переводчики.
Наши ученики в течении 4 месяцев уже свободно владеют языком'''
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Наш Инстаграм", url='https://habr.com/ru/all/')
    markup.add(button1)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def about_usBtn(call):
    if call.message:
        if call.data == 'sign_up_for_lesson':
            print(username)
            add_user(username, firstname)
            bot.send_message(call.message.chat.id, f"{firstname}, Вы записаны на урок!")
        elif call.data == 'show_course':
            # Отправляем 10 кнопок
            markup = types.InlineKeyboardMarkup()
            button_1 = types.InlineKeyboardButton(f'Кнопка 1', callback_data=f'button_1')
            button_2 = types.InlineKeyboardButton(f'Кнопка 2', callback_data=f'button_2')
            button_3 = types.InlineKeyboardButton(f'Кнопка 3', callback_data=f'button_3')
            button_4 = types.InlineKeyboardButton(f'Кнопка 4', callback_data=f'button_4')
            button_5 = types.InlineKeyboardButton(f'Кнопка 5', callback_data=f'button_5')
            button_6 = types.InlineKeyboardButton(f'Кнопка 6', callback_data=f'button_6')
            button_7 = types.InlineKeyboardButton(f'Кнопка 7', callback_data=f'button_7')
            button_8 = types.InlineKeyboardButton(f'Кнопка 8', callback_data=f'button_8')
            button_9 = types.InlineKeyboardButton(f'Кнопка 9', callback_data=f'button_9')
            button_10 = types.InlineKeyboardButton(f'Кнопка 10', callback_data=f'button_10')
            markup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10)
            bot.send_message(call.message.chat.id, 'Вот 10 кнопок:', reply_markup=markup)
        elif call.data.startswith('button_'):
            button_number = int(call.data.split('_')[1])
            bot.send_message(call.message.chat.id, f'Вы нажали кнопку {button_number}')
        elif call.data == 'learn_words':
            pass
        elif call.data == 'english_texts':
            pass


@bot.message_handler(commands=['stop'])
def send_stop(message):
    stop_message = "До свидания! Если вам снова потребуется помощь, просто напишите /start."
    bot.send_message(message.chat.id, stop_message)


bot.polling()
