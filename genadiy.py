import telebot
from telebot.types import Message
import download_agent
import threading
from telegram_agent import parse_chats
import asyncio as io
import dbfile as db

thred_download_agent = threading.Thread(
    target=download_agent.downloader_agent,
    daemon=True)
thred_download_agent.start()

TOKEN = "7393701789:AAGI3lpBeQ3BpkAhjdmNjPWHE84HYDBpEjs"
bot = telebot.TeleBot(TOKEN)
albums = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'привееет!')


@bot.message_handler(commands=['torrent_file'])
def torrent_file(message):
    bot.send_message(message.chat.id,
                     'отправьте фото для будующей аватарки канала: ')
    bot.register_next_step_handler(message, get_photo)


def get_photo(message):
    if message.caption and message.document:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(f"photo/{message.caption + '.' + message.document.file_name.split('.')[-1]}", 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Файл загружен!")
            bot.send_message(message.chat.id, 'отправьте торрент файл: ')
            bot.register_next_step_handler(message, handle_document)
        except Exception as e:
            bot.reply_to(message, f"\033[31;1mОшибка: \033[0m{e}")
    else:
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФОТО' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


def handle_document(message: Message):
    if message.caption and message.document:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(f"torrents/{message.caption}", 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Файл загружен!")
        except Exception as e:
            bot.reply_to(message, f"\033[31;1mОшибка: \033[0m{e}")
    else:
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФАЙЛ' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


@bot.message_handler(commands=['pars'])
def pars(message):
    bot.send_message(
        message.chat.id, 'отправьте ссылку на канал, название будуюего канала и аватарку для будующегго канала: ')
    bot.register_next_step_handler(message, pars_tgk)


def pars_tgk(message):
    if message.caption and message.document:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # try:
        with open(f"photo/{message.caption.split()[-1] + '.' + message.document.file_name.split('.')[-1]}", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Файл загружен!")
        link = message.caption.split()[0]
        channel_name = message.caption.split()[-1]
        bot.send_message(message.chat.id, f'{link}, {channel_name}')
        io.run(parse_chats(
            source_chat=link,
            channel_name=channel_name
        ))
       # except Exception as e:
        #    bot.reply_to(message, f"\033[31;1mОшибка: \033[0m{e}")
    else:
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФОТО' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


@bot.message_handler(content_types=['text'])
def text(message: Message):
    bot.send_message(message.chat.id, '''неизвестная команда :,(''')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_id = photo.file_id
    print(file_id)
    text = message.caption
    db.ChanelService().update_file_id(file_id, int(text))


print('сервер запущен')
bot.polling(non_stop=True, interval=1, timeout=60, long_polling_timeout=60)
