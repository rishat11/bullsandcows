import random
import logging
import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

word = ''
TOKEN = '827159316:AAEcAFng9sYVQHyKcPvzNeoKWUBaCAQo_Bs'
HOST = '54.37.21.29'
PORT = '3128'
REQUEST_KWARGS = {
    'proxy_url': 'http://{}:{}/'.format(HOST, PORT),
}
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

updater = Updater(token=TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


def start(update, context):
    global word
    word_site = "https://raw.githubusercontent.com/hingston/russian/master/10000-russian-words.txt"
    response = requests.get(word_site)
    WORDS = response.content.splitlines()
    WORDS = [decode(x) for x in WORDS if len(decode(x)) == 4 and len(set(decode(x))) == len(decode(x))]
    word = random.choice(WORDS)
    context.bot.send_message(chat_id=update.message.chat_id, text="Я загадал слово!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def decode(string):
    return string.decode('utf-8')


def echo(update, context):
    global word
    message = update.message.text.lower()
    if len(word) == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text="Чтобы начать игру введите команду /start")
    elif len(message) != 4:
        context.bot.send_message(chat_id=update.message.chat_id, text="В загаданном слове 4 буквы.")
    elif len(set(message)) != len(message):
        context.bot.send_message(chat_id=update.message.chat_id, text="В загаданном слове нет повторяющихся букв.")
    elif word == message:
        context.bot.send_message(chat_id=update.message.chat_id, text="Вы угадали!")
        word_site = "https://raw.githubusercontent.com/hingston/russian/master/10000-russian-words.txt"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()
        WORDS = [decode(x) for x in WORDS if len(decode(x)) == 4 and len(set(decode(x))) == len(decode(x))]
        word = random.choice(WORDS)
        context.bot.send_message(chat_id=update.message.chat_id, text="Я загадал слово!")
    else:
        bull, cow = 0, 0
        for idx, item in enumerate(message):
            if message[idx] == word[idx]:
                bull += 1
            if message[idx] in word:
                cow += 1

        context.bot.send_message(chat_id=update.message.chat_id, text="{}:{}".format(cow, bull))


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
