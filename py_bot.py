import logging
import json_work

from telebot import types
import telebot


bot = telebot.TeleBot('5932911207:AAF9tzJRdtoF-hOu83kUeIR3gHvKlUtNccA')


def filter_dialog(record: logging.LogRecord):
    if 'id' in record.getMessage():
        return record.getMessage()


logger = telebot.logger
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot_log.csv', encoding='UTF-8')
handler.setFormatter(logging.Formatter(fmt='[%(levelname)s: %(asctime)s] %(message)s'))
logger.addFilter(filter_dialog)
logger.addHandler(handler)


@bot.message_handler(commands=['start'])
def start(message):
    text_message1 = f'<b><i>Привет, {message.from_user.first_name}!</i></b> \U0001F600'
    text_message2 = f'Этот бот предназначен для выполнения математических операций,\n ' \
                    f'а также же просмотра истории 5 последних действий'
    bot.send_message(message.chat.id, text_message1, parse_mode='html')
    bot.send_message(message.chat.id, text_message2, parse_mode='html')


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    logger_button = types.KeyboardButton('Посмотреть историю')
    markup.add(logger_button)

    if 'start' in get_message_bot:
        bot.send_message(message.chat.id, 'Вводимое не должно быть командой', reply_markup=markup)
    elif 'посмотреть историю' in get_message_bot:
        history(message)
    else:
        try:
            calc = eval(get_message_bot)
            bot.send_message(message.chat.id, f'{get_message_bot} = {calc}', reply_markup=markup)
            json_work.write(message.chat.id, f'{get_message_bot} = {calc}', message.from_user.first_name)
        except SyntaxError:
            bot.send_message(message.chat.id, 'Введите математическое выражение! Например, 2 + 2', reply_markup=markup)


@bot.message_handler(commands=['history'])
def history(message):
    temp_list = json_work.read(message.chat.id)
    for item in temp_list:
        bot.send_message(message.chat.id, item)


print('Бот работает')

bot.polling(none_stop=True)
