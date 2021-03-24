import telebot
from telebot import types
from datetime import time, date, datetime

class UserStudent(object):
    def __init__(self, user_id):
        self.id = user_id
        self.first_launch = True
        self.grade = None
        self.delay = None
        self.history = []

    def set_grade(self, grade):
        self.grade = grade

    def set_delay(self, delay):
        self.delay = delay

    def add_text(self, text):
        self.history += [text]

    def get_history(self):
        return " ".join(self.history)


bot = telebot.TeleBot("1757180443:AAFvzy_6u33CtkNgAcPxpCyA0PCD5hQk2O8")
database = {}

def set_grade_layout(message):
    keyboard = types.InlineKeyboardMarkup(True)
    button_7 = types.InlineKeyboardButton(text="7", callback_data="button_7")
    button_8 = types.InlineKeyboardButton(text="8", callback_data="button_8")
    button_9 = types.InlineKeyboardButton(text="9", callback_data="button_9")
    button_1011 = types.InlineKeyboardButton(text="1011", callback_data="button_1011")
    keyboard.add(button_7, button_8, button_9, button_1011)
    bot.send_message(message.chat.id, "Нажмите кнопку, или введите вручную", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "button_7":
            bot.send_message(call.message.chat.id, "7")
        if call.data == "button_8":
            bot.send_message(call.message.chat.id, "8")
        if call.data == "button_9":
            bot.send_message(call.message.chat.id, "9")
        if call.data == "button_1011":
            bot.send_message(call.message.chat.id, "10-11")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f'Добро пожаловать в школьный чат-бот, {message.from_user.first_name}\n\n' +
                     "Введите, пожалуйста, ваш класс")
    # keyboard = types.InlineKeyboardMarkup()
    # button_7 = types.InlineKeyboardButton(text="7", callback_data="button_7")
    # button_8 = types.InlineKeyboardButton(text="8", callback_data="button_8")
    # button_9 = types.InlineKeyboardButton(text="9", callback_data="button_9")
    # button_1011 = types.InlineKeyboardButton(text="1011",
    #                                          callback_data="button_1011")
    # keyboard.add(button_7)
    # keyboard.add(button_8)
    # keyboard.add(button_9)
    # keyboard.add(button_1011)
    # bot.send_message(message.chat.id, "Нажмите кнопку, или введите вручную",
    #                  reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, f"""Школьный бот v0.07
Доступные команды:
/help - вывод подсказки
/settings - Настройка пользовательских параметров TODO
/remind - Показать историю сообщений
/game - игра TODO
/stop - остановка текущего процесса TODO
/end - отключение от бота TODO""")


@bot.message_handler(commands=['remind'])
def remind(message):
    user_id = message.chat.id
    if user_id in database:
        bot.send_message(user_id, database[user_id].get_history())
    else:
        bot.send_message(user_id, "Вы ещё не писали мне")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text
    user_id = message.chat.id
    print(text, user_id)
    if user_id not in database:
        database[user_id] = UserStudent(user_id=user_id)
    database[user_id].add_text(text)

bot.polling()
