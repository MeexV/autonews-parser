import telebot
import an_parser
from json import load

token = ""  # Токен Tg-бота

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}! Нажми /pars для загрузки новостей!')


@bot.message_handler(commands=['help'])
def help(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Этот бот позволит тебе найти последние новости по автомобильной тематике. Нажми /pars для загрузки новостей!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, обратись за помощью! Напиши /help")


@bot.message_handler(commands=['pars'])
def parsing(message):
    an_parser.parser_news()
    with open('all_news.json', mode='r', encoding='utf-8') as f:
        ans = load(f)
    chat_id = message.chat.id
    for i in ans:
        bot.send_message(chat_id, f"{i['Источник']}")


bot.polling(none_stop=True, interval=0)
