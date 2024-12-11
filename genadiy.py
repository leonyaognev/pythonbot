import telebot
import download_agent
import threading

thred_download_agent = threading.Thread(
    target=download_agent.downloader_agent,
    daemon=True)
thred_download_agent.start()

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
        try:
            with open(f"torrents/{message.document.file_name}", 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Файл загружен!")
        except Exception as e:
            bot.reply_to(message, f"\033[31;1mОшибка: \033[0m{e}")
    else:
        bot.send_message(
            message.chat.id, "нет, ну ты блять ему говоришь 'СКИНЬ ТЫ, СУКА, ФАЙЛ' а он блять берет и какую то поеботу кидает. \n иди нахуй короче, ебанат блядский")


print('сервер запущен')
bot.polling(non_stop=True, interval=1)
