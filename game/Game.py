import random
import logging
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

word_list = open('../dict/word_list', encoding='utf-8')
WORDS = word_list.read().splitlines()
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

updater = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


def start(update, context):
    global word
    word = random.choice(WORDS)
    update.send_message(chat_id=context.message.chat_id, text="Я загадал слово!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(bot, context):
    global word, WORDS
    message = context.message.text.lower()
    if len(word) == 0:
        bot.send_message(chat_id=context.message.chat_id, text="Чтобы начать игру введите команду /start")
    elif message not in WORDS:
        bot.send_message(chat_id=context.message.chat_id, text="В моей базе нет такого слова")
    elif word == message:
        bot.send_message(chat_id=context.message.chat_id, text="Вы угадали!")
        word = random.choice(WORDS)
        bot.send_message(chat_id=context.message.chat_id, text="Я загадал новое слово!")
    else:
        bull, cow = 0, 0
        for idx, item in enumerate(message):
            if message[idx] == word[idx]:
                bull += 1
            if message[idx] in word:
                cow += 1

        bot.send_message(chat_id=context.message.chat_id, text="{}:{}".format(cow, bull))


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
