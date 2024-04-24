import telebot
from telebot import types
TOKEN = '5970535905:AAGWQb0JXkEs9FDjPAjRgkz0xJ1RKF56bvA'
bot = telebot.TeleBot(TOKEN)
user_firstname = None


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
    global user_firstname
    user_firstname = message.from_user.first_name
    welcome_message = "Здравствуйте! Я бот помощник онлайн-школы английского Deshar School.\n" \
                      "Что вас интересует?"
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton("О нас", callback_data='about_us')
    button_2 = types.InlineKeyboardButton('Записаться на урок', callback_data='sign_up_for_lesson')
    button_3 = types.InlineKeyboardButton('Пройти курс', callback_data='show_course')
    button_4 = types.InlineKeyboardButton('Учить слова', callback_data='learn_words')
    button_5 = types.InlineKeyboardButton('Тексты на английском', callback_data='english_texts')
    markup.add(button_1, button_2, button_3, button_4, button_5)
    bot.reply_to(message, welcome_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def about_usBtn(call):
    if call.message:
        if call.data == 'about_us':
            text = f'''Привет, {user_firstname}, мы школа английского Deshar School!
Работаем уже 7 лет, наши преподаватели 15 лет говорят по-английски, аттестованы Кембриджем. Профессиональные переводчики.
Наши ученики в течении 4 месяцев уже свободно владеют языком'''
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Наш Инстаграм", url='https://habr.com/ru/all/')
            markup.add(button1)
            bot.send_message(call.message.chat.id, text, reply_markup=markup)
        elif call.data == 'sign_up_for_lesson':
            bot.send_message(call.message.chat.id, 'Вы записаны на урок')
        elif call.data == 'show_course':
            bot.send_message(call.message.chat.id, 'Доработать')
        elif call.data == 'learn_words':
            pass
        elif call.data == 'english_texts':
            pass


@bot.message_handler(commands=['stop'])
def send_stop(message):
    stop_message = "До свидания! Если вам снова потребуется помощь, просто напишите /start."
    bot.send_message(message, stop_message)


bot.polling()
