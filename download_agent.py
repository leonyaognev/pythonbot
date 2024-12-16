import telegram_agent
import downloader
import threading
import time
import sqlite3
import asyncio as io
import os


class DownloadAgent:
    def __init__(self):
        self.agent_thread = threading.Thread(target=self._agent_routine)
        self.downloader_thread = threading.Thread(
            target=self._downloader_routine)

    def start(self):
        self.agent_thread.start()
        self.downloader_thread.start()

    def _agent_routine(self):
        while True:
            try:
                io.run(telegram_agent.send_all_files())
                time.sleep(10)
            except sqlite3.OperationalError:
                time.sleep(60)

    def _downloader_routine(self):
        while True:
            for file in os.listdir('torrents'):
                io.run(downloader.download(file.split('.')[0]))
                os.system(
                    f'rm -rf /home/ognev/Documents/pythonbot/torrents/{file}')
            time.sleep(10)
