import telegram_agent
import downloader
import threading
import time
import sqlite3
import asyncio as io
import os


def agent():
    while True:
        try:
            io.run(telegram_agent.send_all_files())
            time.sleep(10)
        except sqlite3.OperationalError:
            time.sleep(60)


def downl():
    while True:
        for file in os.listdir('torrents'):
            io.run(downloader.download(file.split('.')[0]))
            os.system(
                f'rm -rf /home/ognev/Documents/pythonbot/torrents/{file}')
        time.sleep(10)


def downloader_agent():
    threadagent = threading.Thread(target=agent)
    threaddownl = threading.Thread(target=downl)

    threadagent.start()
    threaddownl.start()

    threadagent.join()
    threaddownl.join()
