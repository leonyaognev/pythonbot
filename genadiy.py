import telebot
from telebot.types import Message
from rename import rename
from downloader import download
from telegram_agent import send_all_files
import asyncio as io

TOKEN = "7393701789:AAGI3lpBeQ3BpkAhjdmNjPWHE84HYDBpEjs"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'привееет!')


@bot.message_handler(commands=['torrent_file'])
def torrent_file(message):
    bot.send_message(message.chat.id, 'отправьте торрент файл: ')
    bot.register_next_step_handler(message, handle_document)


def handle_document(message):
    if not message.text:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"torrents/{message.document.file_name}", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Файл загружен!")
        io.run(download())
        print('penis')
        bot.reply_to(message, "торрент скачен")
        rename(message.document.file_name.split('.')[0])
        bot.reply_to(message, "файл подкотовлен к выгрузке на сервер")
        io.run(send_all_files())
        bot.reply_to(message, "все файлы отправлены, тгк готов!")
    else:
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФАЙЛ' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


print('сервер запущен')
bot.polling(non_stop=True, interval=1)
