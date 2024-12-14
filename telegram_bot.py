import telebot
from telebot import types
from telebot.types import Message
from search import search_link, lexemes
import dbfile as db
import json as js

TOKEN = "7905948999:AAG2Clgv7gNyAgqiXVSuKcJgjY86tqJX0lM"
bot = telebot.TeleBot(TOKEN)

bot_last_message = {}
main_file = 'AgACAgIAAxkBAANIZ2XErhbG2zBAIssejtrqYSbazTUAAsXmMRs0rDBLNFHle7tDRJcBAAMCAAN5AAM2BA'
search_file = 'AgACAgIAAxkBAANqZ2XWUEvuw5yXTttp7bva2Afkf7oAAgHsMRuM9ChLm_ioN8nH6L8BAAMCAAN4AAM2BA'


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
    bot_last_message[call.message.chat.id] = [call.message]
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    file = main_file
    if call.data == 'back':
        main_menu(call)
        return
    if call.data == 'search':
        file = search_file
        text = 'введите название искомого сериала: '
        but1 = telebot.types.InlineKeyboardButton(
            'вернуться в главное меню', callback_data=('back')
        )
        keyboard.add(but1)
        bot.register_next_step_handler(call.message, search)

    if call.data == 'random':
        channel = db.ChanelService().random_serial()
        file_page(call.message, channel)
        return

    if call.data == 'sav':
        text = 'созраненные сериалы:'
        but1 = telebot.types.InlineKeyboardButton(
            'вернуться в главное меню', callback_data=('back')
        )
        keyboard.add(but1)

    if call.data == 'donate':
        text = 'разраб сосет бебру и очень этим доволен, так что не надо кидать ему никаких денег, лучше помолитесь за него в церкви)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))'
        but1 = telebot.types.InlineKeyboardButton(
            'вернуться в главное меню', callback_data=('back')
        )
        keyboard.add(but1)

    if call.data.startswith('file_page'):
        channel = db.ChanelService().get_by_id(int(call.data.split('|')[-1]))
        file_page(call.message, channel)
        return

    if call.data.startswith('save'):
        channel = db.ChanelService().get_by_id(int(call.data.split('|')[-1]))
        save(call.message, channel.id)
        return

    if call.data.startswith('delete'):
        channel = db.ChanelService().get_by_id(int(call.data.split('|')[-1]))
        delete(call.message, channel.id)
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
    media = types.InputMediaPhoto(main_file, caption=text)
    bot.edit_message_media(
        media=media,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def search(message: Message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    channels = search_link(lexemes(message.text.replace(' ', '-')))
    if channels:
        for channel in channels:
            text = 'найденые результаты'
            but = telebot.types.InlineKeyboardButton(
                f'{channel.chanelname}',
                callback_data=(f'file_page|{channel.id}')
            )
            keyboard.add(but)
    else:
        text = 'извните, ничего не найдено :,('
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

    text = channel.chanelname
    url = channel.invitelink
    file_id = channel.file_id

    but1 = telebot.types.InlineKeyboardButton(
        text,
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


def save(message, channel_id):
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


def delete(message, channel_id):
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


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_id = photo.file_id
    bot.send_message(message.chat.id, file_id)


print('сервер запущен')
bot.polling(non_stop=True, interval=1, timeout=99999999,
            long_polling_timeout=99999999)
