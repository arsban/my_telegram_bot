import os
import telegram
from telegram import message
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import moviepy.editor as mp
from random import randint
import random

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

COMAND_ANSWERS = {
    'start': 'Привет {}!\nспасибо что присоединился к my_bot',
    'help': (
        'Бот умеет принимать аудио/видеофайлы, фото,\n'
        'текстовые сообщения и команды которые начинаются с "/"\n'
        'если он что-то не может, он ответит вам честно\n'
        'команда /random_digit - это игра в кости, при нажатии вам выпадет число от 1 до 6\n'
        'команда /YesOrNo - дас вам ответ на извечный вопрос - "ДА" или "НЕТ"'
        ),
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='telegram_bot.log',
    datefmt='%Y-%m-%d, %H:%M:%S',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w',
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler_rotate = RotatingFileHandler(
    'telegram_bot.log',
    maxBytes=50_000_000,
    backupCount=5,
)
handler_stream = logging.StreamHandler()
logger.addHandler(handler_rotate)
logger.addHandler(handler_stream)


bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)
dp = updater.dispatcher


def send_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def text_message_controler(update, context):
    chat = update.effective_chat
    text_mesage = update.message.text
    context.bot.send_message(chat_id=chat.id, text=f'Я не понимаю: {text_mesage} - не запрограмирован еще:(')
    # send_message("Я пока не умею обрабатывать эту команду :(")

def photo_message_controler(update, context):
    send_message("Я пока не умею обрабатывать фотографии :(")

def video_message_controler(update, context):
    chat = update.effective_chat
    videofile = update.message.video
    # vid_for_aud_conv = mp.VideoFileClip(videofile)
    context.bot.send_message(chat_id=chat.id, text=f"Ты отправил видефайл: {videofile}")
    # send_message("Я пока не умею обрабатывать видеофайлы:(")


def audio_message_controler(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Я пока не умею обрабатывать аудиофайлы :(")

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([
        ['/menu', '/help'],
        ['/random_digit'], ['/YesOrNo'],  #назвать это игрой в кости
        ['Кнопка1'], ['Кнопка2'],
        ['Кнопка3', 'Кнопка4'],
    ])
    context.bot.send_message(chat_id=chat.id, text=COMAND_ANSWERS['start'].format(name), reply_markup=button)
    
    

def help_text(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=COMAND_ANSWERS['help'])

def random_digit(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id, text=f"{name} выбрасывает число: {randint(1, 6)}")

def yes_or_no(update, context):
    chat = update.effective_chat
    Yes_Or_No = ['Yes', 'No']
    context.bot.send_message(chat_id=chat.id, text=f"{random.choice(Yes_Or_No)}")

################
# тут обрабатываются команды с "/" например "/start" и "/help"
dp.add_handler(CommandHandler('start', wake_up))
dp.add_handler(CommandHandler('help', help_text))
dp.add_handler(CommandHandler('random_digit', random_digit))
dp.add_handler(CommandHandler('YesOrNo', yes_or_no))
################
################
# тут обрабатываются текстовые сообщения (str) и разные типы файлов.
dp.add_handler(MessageHandler(Filters.text, text_message_controler))
dp.add_handler(MessageHandler(Filters.photo, photo_message_controler))
dp.add_handler(MessageHandler(Filters.video, video_message_controler))
dp.add_handler(MessageHandler(Filters.audio, audio_message_controler))
################
# Метод start_polling() запускает процесс polling, 
# приложение начнёт отправлять регулярные запросы для получения обновлений.
# параметр poll_interval обозначает нужный интервал запросов (в секундах, float)
updater.start_polling(poll_interval=5.0)
################
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
################