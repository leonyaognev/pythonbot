import re
import json as js
import telebot
import asyncio as io

from telebot.types import Message
from telegram_agent import parse_chats, rename_parsed_messages

from download_agent import DownloadAgent


TOKEN = "7393701789:AAGI3lpBeQ3BpkAhjdmNjPWHE84HYDBpEjs"
bot = telebot.TeleBot(TOKEN)
authorized_users = list()

processing_command = False


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'привееет!')


@bot.message_handler(commands=['authorization'])
def authorization_hendler(message):
    if str(message.chat.id) in authorized_users:
        bot.send_message(
            message.chat.id, 'ебанат, так ты же уже и так авторизован, \
нахуй заново пытыешься \
авторизоваться?\nебанат блять...')
        return
        bot.register_next_step_hendler(message, authorization_hendler)
    bot.send_message(message.chat.id, 'введите пароль админа:')
    bot.register_next_step_handler(message, check_authorization)


def check_authorization(message):
    if not message.text:
        bot.send_message(
            message.chat.id, 'извините, но вы отправили мне какую то поеботу, идите нахуй блять с такими преколоми, вы пидорас, я ваш рот ебал и мамашу вашу потрахивал смачнейше')
    global authorized_users

    password = message.text

    if password == 'oralcumshot':
        if not (str(message.chat.id) in authorized_users):
            authorized_users.append(str(message.chat.id))

            with open('authorized_users.json', 'w') as data:
                js.dump(authorized_users, data)

            bot.send_message(
                message.chat.id, 'поздравляю, вы успешно авторизованы!')
    else:
        bot.send_message(message.chat.id, 'ага блять, так я теба и пропутил, \
иди нахуй, сучка, мамаше там своей поплачь, я хз. \
ах да, кстати, я ебал её вчера и сегодня \
вечерком пару раз её выбe блять, сучка')


@bot.message_handler(commands=['create_new_channel'])
def create_handler(message):
    global authorized_users
    if not (str(message.chat.id) in authorized_users):
        bot.send_message(
            message.chat.id, 'ага блять, иди нахуй сука падаль неавторизованная')
        return

    global processing_command

    if processing_command:
        bot.send_message(
            message.chat.id,
            'Какая-то другая комманда уже в обработке.'
        )
        return

    processing_command = True
    bot.send_message(message.chat.id, 'Отправьте имя канала:')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    # Check for text
    if not message.text:
        bot.send_message(
            message.chat.id, "Пустое сообщение.\nОтправьте имя канала:")
        bot.register_next_step_handler(message, get_name)
        return

    # Extract name and delete message
    channel_name = message.text

    # Validate name format
    if not re.match(r"^\w+(-\w+){0,}$", channel_name):
        bot.send_message(
            message.chat.id,
            "Неверый формат имени. Имя должно соответсвовать формату 'имя-канала'.\nОтправьте имя канала:"
        )
        bot.register_next_step_handler(message, get_name)
        return

    bot.send_message(message.chat.id, "Отправьте описание канала:")

    info = {"channel_name": channel_name}

    bot.register_next_step_handler(message, get_caption, info)


def get_caption(message, info):
    # Check for text
    if not message.text:
        bot.send_message(
            message.chat.id,
            "Пустое сообщение.\nОтправьте описание канала:"
        )
        bot.register_next_step_handler(message, get_caption, info)
        return

    # Check len caption
    if len(message.text) > 800:
        bot.send_message(
            message.chat.id,
            "Ты ебанатище, подпис слишком длинная, давай че нить покороче")

    # Extract channel caption and delete message
    channel_caption = message.text
    info["channel_caption"] = channel_caption

    # Next step
    bot.send_message(message.chat.id, "Отправьте аватарку канала:")
    bot.register_next_step_handler(message, get_cover, info)


def get_cover(message, info):
    # Check for document
    if not message.document:
        bot.send_message(
            message.chat.id,
            "Сообщение не содержит файла.\nОтправьте аватарку канала:"
        )
        bot.register_next_step_handler(message, get_cover, info)
        return

    # Extract channel cover
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    channel_cover = bot.download_file(file_info.file_path)

    file_extension = message.document.file_name.split('.')[-1]

    info["channel_cover"] = channel_cover
    info["channel_cover_extension"] = file_extension

    # Next step
    bot.send_message(
        message.chat.id, "Отправьте ссылку на канал источник или торрент файл:")

    bot.register_next_step_handler(
        message, get_source_channel_link, info)


def get_source_channel_link(message, info):
    if message.text:
        # Extract channel link
        source_channel_link = message.text
        info["source_channel_link"] = source_channel_link

        # Next step
        bot.send_message(message.chat.id, "Парсим канал...")
        parse(message, info)

    elif message.document:
        # Extract torrent file
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        torrent_file = bot.download_file(file_info.file_path)

        info["torrent_file"] = torrent_file
        # Next step
        bot.send_message(
            message.chat.id,
            "Отправьте номер сезона (если в файле сезонов больше одного отправьте 0):"
        )

        bot.register_next_step_handler(message, get_season_number,
                                       info)

    else:
        bot.send_message(
            message.chat.id,
            "Пустое сообщение.\nОтправьте ссылку на канал-источник или торрент файл:"
        )
        bot.register_next_step_handler(message, get_source_channel_link,
                                       info)
        return


def get_season_number(message, info):
    if not message.text or not message.text.isdigit():
        bot.send_message(
            message.chat.id,
            "Пустое сообщение.\nОтправьте номер сезона:"
        )
        bot.register_next_step_handler(message, get_season_number,
                                       info)
        return

    if int(message.text) < 0:
        bot.send_messge(message.chat.id, 'номер сезон отрицательный')
        bot.register_next_step_handler(message, get_season_number,
                                       info)

    # Extract season
    info['season'] = message.text

    # Next step
    bot.send_message(message.chat.id, 'начинаю скачивание торрента...')
    download_torrent(message, info)


def download_torrent(message, info):
    global processing_command

    try:
        # Download cover
        cover_file_name = f"photo/{info['channel_name']
                                   }.{info['channel_cover_extension']}"

        with open(cover_file_name, 'wb') as new_file:
            new_file.write(info["channel_cover"])

        bot.send_message(message.chat.id, "Обложка загружена.")

        # Save torrent
        if int(info['seaso']):
            with open(f"torrents/{info['season']} {info['channel_name']}", 'wb') as new_file:
                new_file.write(info['torrent_file'])

        else:
            with open(f"torrents/{info['name']}", 'wb') as new_file:
                new_file.write(info['torrent_file'])

        bot.send_message(message.chat.id, "Торрент файл загружен")

        # Save caption
        with open('caption.json', 'r') as data:
            penis = js.load(data)

        if not (info["channel_name"] in info["channel_caption"]):
            penis[info["channel_name"]] = info["channel_caption"]

        with open('caption.json', 'w') as data:
            js.dump(penis, data)

    except Exception as e:
        bot.reply_to(message, f"Ошибка:\n{e}")

    processing_command = False


def parse(message, info):
    global processing_command

    try:
        # Download cover
        cover_file_name = f"photo/{info['channel_name']
                                   }.{info['channel_cover_extension']}"

        with open(cover_file_name, 'wb') as new_file:
            new_file.write(info["channel_cover"])

        bot.send_message(message.chat.id, "Обложка загружена.")

        # Save caption
        with open('caption.json', 'r') as data:
            penis = js.load(data)

        if not (info["channel_name"] in info["channel_caption"]):
            penis[info["channel_name"]] = info["channel_caption"]

        with open('caption.json', 'w') as data:
            js.dump(penis, data)

        # Parse chat
        channel_id = io.run(parse_chats(
            source_chat=info["source_channel_link"],
            channel_name=info["channel_name"]
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
    if not (str(message.chat.id) in authorized_users):
        bot.send_message(
            message.chat.id, 'ага блять, иди нахуй сука падаль неавторизованная')
        return
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

    try:
        text = message.text.split()
        res = io.run(rename_parsed_messages(
            int(text[0]), int(text[1]), *text[2:]))
        if res:
            bot.send_message(message.chat.id, 'хуй залупа все готово')
        else:
            bot.send_message(
                message.chat.id, 'братан, чет поебота какая то, может ты чет не то скинул мне, ебанат?')

        processing_command = False
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
        processing_command = False


@bot.message_handler(content_types=['text'])
def text(message: Message):
    if not (str(message.chat.id) in authorized_users):
        bot.send_message(
            message.chat.id, 'ага блять, иди нахуй сука падаль неавторизованная')
        return

    bot.send_message(message.chat.id, 'неизвестная команда :,(')


def get_authorized_users():
    global authorized_users

    with open('authorized_users.json', 'r') as data:
        penis = js.load(data)
    authorized_users = penis


def main():
    print('downloader agenjjjjt запущен')
    download_agent = DownloadAgent()
    download_agent.start()

    print('генадий запущен')
    get_authorized_users()
    bot.polling(non_stop=True, interval=1, timeout=9999999,
                long_polling_timeout=9999999)


if __name__ == "__main__":
    main()
