import telebot
from telebot.types import Message
from search import search_link, lexemes

TOKEN = "7582842855:AAFTXLRxH5HmNQ8eQUSHbZPUebQzvswg-4Y"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'привееет!')


@bot.message_handler(commands=['search'])
def handle_search(message):
    bot.send_message(
        message.chat.id,
        'введите название искомого фильма/сериала: '
    )
    bot.register_next_step_handler(message, search)


def search(message: Message):
    links = search_link(lexemes(message.text))
    if links:
        for link in links:
            bot.send_message(
                message.chat.id,
                f'{link}'
            )
    else:
        bot.send_message(
            message.chat.id,
            'извните, ничего не найдено :,('
        )


@bot.message_handler(content_types=['text'])
def text(message: Message):
    bot.send_message(message.chat.id, '''неизвестная команда :,(''')


print('сервер запущен')
bot.polling(non_stop=True, interval=1)
