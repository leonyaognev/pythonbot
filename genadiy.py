import re
import json as js
import telebot
import asyncio as io

from telebot.types import Message
from telegram_agent import parse_chats, rename_parsed_messages

from download_agent import DownloadAgent


TOKEN = "7393701789:AAGI3lpBeQ3BpkAhjdmNjPWHE84HYDBpEjs"
bot = telebot.TeleBot(TOKEN)
albums = {}

processing_command = False


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'привееет!')


@bot.message_handler(commands=['torrent_file'])
def get_caption(message):
    global processing_command

    if processing_command:
        bot.send_message(
            message.chat.id,
            'Какая-то другая комманда уже в обработке.'
        )
        return

    processing_command = True
    bot.send_message(message.chat.id,
                     'отправьте подпись канала: ')
    bot.register_next_step_handler(message, torrent_file)


def torrent_file(message):
    with open('caption.json', 'r') as data:
        penis = js.load(data)
    channel_name = message.text.split()[0]
    caption = ' '.join(message.text.split()[1:])
    if not (channel_name in penis):
        penis[channel_name] = caption
    with open('caption.json', 'w') as data:
        js.dump(penis, data)

    bot.send_message(message.chat.id,
                     'отправьте фото для будующей аватарки канала: ')
    bot.register_next_step_handler(message, get_photo)


def get_photo(message):
    global processing_command

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
            processing_command = False
            bot.reply_to(message, f"\033[31;1mОшибка: \033[0m{e}")
    else:
        processing_command = False
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФОТО' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


def handle_document(message: Message):
    global processing_command

    if message.caption and message.document:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(f"torrents/{message.caption}", 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Файл загружен!")
        except Exception as e:
            processing_command = False
            bot.reply_to(message, f"\033[31;1mОшибка: \033[0m{e}")
    else:
        processing_command = False
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФАЙЛ' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


@bot.message_handler(commands=['parse'])
def parse_handler(message):
    global processing_command

    if processing_command:
        bot.send_message(
            message.chat.id,
            'Какая-то другая комманда уже в обработке.'
        )
        return

    processing_command = True
    bot.send_message(message.chat.id, 'Отправьте имя канала:')
    bot.register_next_step_handler(message, parse_get_name)


def parse_get_name(message):
    # Check for text
    if not message.text:
        bot.send_message(
            message.chat.id, "Пустое сообщение.\nОтправьте имя канала:")
        bot.register_next_step_handler(message, parse_get_name)
        return

    # Extract name and delete message
    channel_name = message.text

    # Validate name format
    if not re.match(r"^\w+(-\w+){1,}$", channel_name):
        bot.send_message(
            message.chat.id,
            "Неверый формат имени. Имя должно соответсвовать формату 'имя-канала'.\nОтправьте имя канала:"
        )
        bot.register_next_step_handler(message, parse_get_name)
        return

    bot.send_message(message.chat.id, "Отправьте описание канала:")

    parse_info = {"channel_name": channel_name}

    bot.register_next_step_handler(message, parse_get_caption, parse_info)


def parse_get_caption(message, parse_info):
    # Check for text
    if not message.text:
        bot.send_message(
            message.chat.id,
            "Пустое сообщение.\nОтправьте описание канала:"
        )
        bot.register_next_step_handler(message, parse_get_caption, parse_info)
        return

    # Extract channel caption and delete message
    channel_caption = message.text
    parse_info["channel_caption"] = channel_caption

    # Next step
    bot.send_message(message.chat.id, "Отправьте аватарку канала:")
    bot.register_next_step_handler(message, parse_get_cover, parse_info)


def parse_get_cover(message, parse_info):
    # Check for document
    if not message.document:
        bot.send_message(
            message.chat.id,
            "Сообщение не содержит файла.\nОтправьте аватарку канала:"
        )
        bot.register_next_step_handler(message, parse_get_cover, parse_info)
        return

    # Extract channel cover
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    channel_cover = bot.download_file(file_info.file_path)

    file_extension = message.document.file_name.split('.')[-1]

    parse_info["channel_cover"] = channel_cover
    parse_info["channel_cover_extension"] = file_extension

    # Next step
    bot.send_message(message.chat.id, "Отправьте ссылку на канал источник:")

    bot.register_next_step_handler(
        message, parse_get_source_channel_link, parse_info)


def parse_get_source_channel_link(message, parse_info):
    # Check for text
    if not message.text:
        bot.send_message(
            message.chat.id,
            "Пустое сообщение.\nОтправьте ссылку на канал-источник:"
        )
        bot.register_next_step_handler(message, parse_get_source_channel_link,
                                       parse_info)
        return

    # Extract channel link
    source_channel_link = message.text
    parse_info["source_channel_link"] = source_channel_link

    # Next step
    bot.send_message(message.chat.id, "Парсим канал...")
    parse(message, parse_info)


def parse(message, parse_info):
    global processing_command

    try:
        # Download cover
        cover_file_name = f"photo/{parse_info['channel_name']
                                   }.{parse_info['channel_cover_extension']}"

        with open(cover_file_name, 'wb') as new_file:
            new_file.write(parse_info["channel_cover"])

        bot.send_message(message.chat.id, "Обложка загружена.")

        # Save caption
        with open('caption.json', 'r') as data:
            penis = js.load(data)

        if not (parse_info["channel_name"] in parse_info["channel_caption"]):
            penis[parse_info["channel_name"]] = parse_info["channel_caption"]

        with open('caption.json', 'w') as data:
            js.dump(penis, data)

        # Parse chat
        channel_id = io.run(parse_chats(
            source_chat=parse_info["source_channel_link"],
            channel_name=parse_info["channel_name"]
        ))

        bot.send_message(
            message.chat.id,
            f'Парсинг канала успешно заверщён. ID канала: {channel_id}'
        )
    except Exception as e:
        bot.reply_to(message, f"Ошибка:\n{e}")

    processing_command = False


@bot.message_handler(commands=['format'])
def format_handler(message):
    global processing_command

    if processing_command:
        bot.send_message(
            message.chat.id,
            'Какая-то другая комманда уже в обработке.'
        )
        return

    processing_command = True
    bot.send_message(
        message.chat.id, 'отправьте id канала, количество сезонов, \
                и сколько серий в каждом из них')
    bot.register_next_step_handler(message, format)


def format(message):
    global processing_command

    text = message.text.split()
    res = io.run(rename_parsed_messages(int(text[0]), int(text[1]), *text[2:]))
    if res:
        bot.send_message(message.chat.id, 'хуй залупа все готово')
    else:
        bot.send_message(
            message.chat.id, 'братан, чет поебота какая то, может ты чет не то скинул мне, ебанат?')

    processing_command = False


@bot.message_handler(content_types=['text'])
def text(message: Message):
    bot.send_message(message.chat.id, 'неизвестная команда :,(')


def main():
    print('downloader agent запущен')
    download_agent = DownloadAgent()
    download_agent.start()

    print('генадий запущен')
    bot.polling(non_stop=True, interval=1, timeout=60,
                long_polling_timeout=60)


if __name__ == "__main__":
    main()
