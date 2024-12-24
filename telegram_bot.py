import telebot
from telebot import types
from telebot.types import Message
from search import search_link, lexemes
import dbfile as db
import json as js
import asyncio as io

import time

TOKEN = "7905948999:AAG2Clgv7gNyAgqiXVSuKcJgjY86tqJX0lM"
bot = telebot.TeleBot(TOKEN)

bot_last_message = {}
content_types = ["text", "audio", "document", "sticker", "video",
                 "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title",
                 "new_chat_photo", "delete_chat_photo", "group_chat_created",
                 "supergroup_chat_created", "channel_chat_created",
                 "migrate_to_chat_id", "migrate_from_chat_id",
                 "pinned_message", "web_app_data"]
main_file = 'AgACAgIAAxkBAANIZ2XErhbG2zBAIssejtrqYSbazTUAAsXmMRs0rDBLNFHle7tDRJcBAAMCAAN5AAM2BA'
search_file = 'AgACAgIAAxkBAANqZ2XWUEvuw5yXTttp7bva2Afkf7oAAgHsMRuM9ChLm_ioN8nH6L8BAAMCAAN4AAM2BA'
donate_file = 'AgACAgIAAxkBAAOZZ2bh6C9r2ZwpZXpV0Juapy00oTsAAmXkMRudSTlLHeQ3exBc2rMBAAMCAAN5AAM2BA'
search_state = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    text = 'главное меню'
    but1 = telebot.types.InlineKeyboardButton(
        'поиск по названию', callback_data='search')
    but2 = telebot.types.InlineKeyboardButton(
        'рандомный сериал', callback_data='random')
    but3 = telebot.types.InlineKeyboardButton(
        'избранные сериалы', callback_data='sav')
    but4 = telebot.types.InlineKeyboardButton(
        'донат)))', callback_data='donate')
    keyboard.add(but1, but2, but3, but4)
    bot.send_photo(
        caption=text,
        chat_id=message.chat.id,
        reply_markup=keyboard,
        photo=main_file)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global search_state
    bot_last_message[call.message.chat.id] = [call.message]
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    file = main_file
    search_state[str(call.message.chat.id)] = False

    if call.data == 'back':
        keyboard, file, text = main_menu(call)

    if call.data == 'search':
        search_state[str(call.message.chat.id)] = True
        file = search_file
        text = 'введите название искомого сериала: '
        but1 = telebot.types.InlineKeyboardButton(
            'вернуться в главное меню', callback_data=('back')
        )
        keyboard.add(but1)
        bot.register_next_step_handler(
            call.message, search)

    if call.data == 'random':
        channel = db.ChanelService().random_serial()
        keyboard, file, text = file_page(call.message, channel)
        but = telebot.types.InlineKeyboardButton(
            'ещё рандомный сериал', callback_data='random')
        keyboard.__dict__['keyboard'].insert(2, [but])

    if call.data == 'sav':
        text = 'сохраненные сериалы:'
        keyboard = get_seved_channels(call.message, keyboard)

    if call.data == 'donate':
        text = 'разраб сосет бебру и очень этим доволен, так что не надо кидать ему никаких денег, лучше помолитесь за него в церкви)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))'
        file = donate_file
        but1 = telebot.types.InlineKeyboardButton(
            'вернуться в главное меню', callback_data=('back')
        )
        keyboard.add(but1)

    if call.data.startswith('file_page'):
        channel = db.ChanelService().get_by_id(int(call.data.split('|')[-1]))
        keyboard, file, text = file_page(call.message, channel)

    if call.data.startswith('save'):
        channel = db.ChanelService().get_by_id(int(call.data.split('|')[-1]))
        io.run(save(call.message, channel.id))
        return

    if call.data.startswith('delete'):
        channel = db.ChanelService().get_by_id(int(call.data.split('|')[-1]))
        io.run(delete(call.message, channel.id))
        return

    media = types.InputMediaPhoto(file, caption=text)
    bot.edit_message_media(
        media=media,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def main_menu(call):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    text = 'главное меню'
    but1 = telebot.types.InlineKeyboardButton(
        'поиск по названию', callback_data='search')
    but2 = telebot.types.InlineKeyboardButton(
        'рандомный сериал', callback_data='random')
    but3 = telebot.types.InlineKeyboardButton(
        'избранные сериалы', callback_data='sav')
    but4 = telebot.types.InlineKeyboardButton(
        'донат)))', callback_data='donate')
    keyboard.add(but1, but2, but3, but4)
    return keyboard, main_file, text


def search(message: Message):
    if not search_state[str(message.chat.id)]:
        bot.delete_message(message.chat.id, message.id)
        return

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    if not message.text or len(message.text) > 100:
        text = 'некорректное название искомого сериала'
        bot.register_next_step_handler(
            message, search)
    else:
        channels = search_link(lexemes(message.text.replace(' ', '-')))
        if channels:
            for channel in channels:
                text = 'найденые результаты'
                but = telebot.types.InlineKeyboardButton(
                    f'{channel.chanelname.replace("-", " ")}',
                    callback_data=(f'file_page|{channel.id}')
                )
                keyboard.add(but)
        else:
            text = 'извните, ничего не найдено :,('
            bot.register_next_step_handler(
                message, search)
    but1 = telebot.types.InlineKeyboardButton(
        'вернуться в главное меню', callback_data=('back')
    )
    bot.delete_message(message.chat.id, message.id)
    message = bot_last_message[message.chat.id][0]
    keyboard.add(but1)
    media = types.InputMediaPhoto(search_file, caption=text)
    bot.edit_message_media(
        media=media,
        chat_id=message.chat.id,
        message_id=message.id,
        reply_markup=keyboard
    )


def file_page(message, channel: db.Chanel):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    text = f'название: {channel.chanelname.replace(
        '-', ' ')}\n\nописание: {channel.caption}'
    url = channel.invitelink
    file_id = channel.file_id

    but1 = telebot.types.InlineKeyboardButton(
        f'смотреть: {channel.chanelname.replace('-', ' ')}',
        url=url
    )

    if not save_in_user(message, channel.id):
        but2 = telebot.types.InlineKeyboardButton(
            'добавить в избранное', callback_data=(f'save|{channel.id}')
        )
    else:
        but2 = telebot.types.InlineKeyboardButton(
            'удалить из избранного', callback_data=(f'delete|{channel.id}')
        )

    but3 = telebot.types.InlineKeyboardButton(
        'вернуться в главное меню', callback_data=('back')
    )
    keyboard.add(but1, but2, but3)

    return keyboard, file_id, text

    media = types.InputMediaPhoto(file_id, caption=text)
    bot.edit_message_media(
        media=media,
        chat_id=message.chat.id,
        message_id=message.id,
        reply_markup=keyboard
    )


def save_in_user(message, channel_id):
    with open('users_save.json') as data:
        penis = js.load(data)
    message = str(message.chat.id)
    if not (message in penis):
        penis[message] = list()
    return True if channel_id in penis[message] else False


async def save(message, channel_id):
    with open('users_save.json', 'r') as data:
        penis = js.load(data)
    mes = str(message.chat.id)
    if not (mes in penis):
        penis[mes] = set()
    penis[mes] = set(penis[mes])
    penis[mes].add(channel_id)
    penis[mes] = list(penis[mes])

    with open('users_save.json', 'w') as data:
        js.dump(penis, data)

    new_button = telebot.types.InlineKeyboardButton(
        'удалить из избранного', callback_data=(f'delete|{channel_id}')
    )
    update_button(bot, message, new_button, row=1, col=0)


async def delete(message, channel_id):
    with open('users_save.json', 'r') as data:
        penis = js.load(data)

    mes = str(message.chat.id)
    if not (mes in penis):
        penis[mes] = set()
    penis[mes] = set(penis[mes])
    penis[mes].discard(channel_id)
    penis[mes] = list(penis[mes])

    with open('users_save.json', 'w') as data:
        js.dump(penis, data)

    new_button = telebot.types.InlineKeyboardButton(
        'добавить в избранное', callback_data=(f'save|{channel_id}')
    )
    update_button(bot, message, new_button, row=1, col=0)


def update_button(bot, message, new_button, row, col):
    keyboard = message.reply_markup.keyboard
    keyboard[row][col] = new_button
    updated_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.id,
        reply_markup=updated_markup)


def get_seved_channels(message, keyboard):
    with open('users_save.json', 'r') as data:
        penis = js.load(data)

    if not (str(message.chat.id) in penis):
        penis[str(message.chat.id)] = list()
    for channel_id in penis[str(message.chat.id)]:
        chan = db.ChanelService().get_by_id(channel_id)
        but = telebot.types.InlineKeyboardButton(
            chan.chanelname.replace('-', ' '), callback_data=(f'file_page|{chan.id}')
        )
        keyboard.add(but)
    but = telebot.types.InlineKeyboardButton(
        'вернуться в главное меню', callback_data=('back')
    )
    keyboard.add(but)
    return keyboard


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.id == 1747419175 and message.caption and message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        text = message.caption
        db.ChanelService().update_file_id(file_id, int(text))
        bot.delete_message(message.chat.id, message.id)
    else:
        bot.delete_message(message.chat.id, message.id)


@bot.message_handler(content_types=content_types)
def del_all_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    but1 = telebot.types.InlineKeyboardButton(
        'поиск по названию', callback_data='search')
    but2 = telebot.types.InlineKeyboardButton(
        'рандомный сериал', callback_data='random')
    but3 = telebot.types.InlineKeyboardButton(
        'избранные сериалы', callback_data='sav')
    but4 = telebot.types.InlineKeyboardButton(
        'донат)))', callback_data='donate')
    keyboard.add(but1, but2, but3, but4)
    for i in range(30):
        try:
            channel = db.ChanelService().get_by_id(i)
            bot.send_photo(
                caption=f"название: {
                    channel.chanelname}\n\nописание: {channel.caption}",
                chat_id=message.chat.id,
                reply_markup=keyboard,
                photo=channel.file_id)
        except Exception as e:
            if channel:
                print(channel.id)
            print(e)
    bot.delete_message(message.chat.id, message.id)


print('сервер запущен')
bot.polling(non_stop=True, interval=1, timeout=99999999,
            long_polling_timeout=99999999)
