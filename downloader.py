from rename import rename
import os
import asyncio
import qbittorrent as qbt
import time
import asyncio as io

FINISHED_TORRENTS_FILE_NAME = ".finished-torrents.txt"
DOWNLOADS_DIR_NAME = "downloads"
TORRENT_FILES_DIR_NAME = "torrents"


qbt_client = None
tg_bot = None


def setup_working_directory() -> None:
    """
    This function creates folders and files, required for bot work
    """
    print("Подготовка рабочей директории...")

    if not os.path.isfile(FINISHED_TORRENTS_FILE_NAME):
        finished_torrents_file = open(FINISHED_TORRENTS_FILE_NAME, "w")
        finished_torrents_file.close()

    if not os.path.isdir(DOWNLOADS_DIR_NAME):
        os.mkdir(DOWNLOADS_DIR_NAME)

    print("Рабочая директория готова к работе.")


def init_qbt_client() -> None:
    """ Initializes qbt client """
    global qbt_client

    print("Регистрирую qbittorrent клиент...")

    qbt_client = qbt.Client("http://127.0.0.1:8080")
    qbt_client.login("admin", "penispenis")

    print("Qbittorent клиент успешно зарегистрирован.")


def init() -> None:
    """ Initializes everything what we need to start work """
    setup_working_directory()
    init_qbt_client()


def download_torrent(filepath: str, outdir: str) -> str:
    """ Starts torrent download """
    print(f"Начинаю скачивать {filepath}.")
    torrent_file = open(filepath, "rb")
    qbt_client.download_from_file(torrent_file, savepath=DOWNLOADS_DIR_NAME)
    torrent_file.close()

    while True:
        torrents = qbt_client.torrents()
        assert len(torrents) == 1

        torrent = torrents[0]
        print(f"{torrent['name']}: {torrent['progress']*100:.0f}%", end="\r")

        if torrent["progress"] == 1:
            break
        time.sleep(1)

    qbt_client.delete(torrent['hash'])

    return torrent['content_path']


async def download(massage) -> None:
    """ Main entry point """
    init()

    finished_torrents_list_file = open(FINISHED_TORRENTS_FILE_NAME, "r")
    finished_torrent_filepaths = finished_torrents_list_file.readlines()
    finished_torrents_list_file.close()

    torrent_files = [f for f in os.listdir(
        TORRENT_FILES_DIR_NAME) if f not in finished_torrent_filepaths]
    if len(torrent_files) == 0:
        print("Нет файлов на скачивание.")
        return

    print("\n==== Очередь на скачивание ====")
    for i in range(len(torrent_files)):
        print(f'\033[34m{i+1}.\033[0m {torrent_files[i]}')
    print()

    for torrent_file in torrent_files:
        torrent_dir = download_torrent(TORRENT_FILES_DIR_NAME + "/" + torrent_file,
                                       DOWNLOADS_DIR_NAME)

        finished_torrents_list_file = open(FINISHED_TORRENTS_FILE_NAME, "a")
        finished_torrents_list_file.write(torrent_file)
        finished_torrents_list_file.close()
    print("Все торренты из спика успешно загружены.")

    while len(os.listdir('/home/ognev/Documents/pythonbot/files/')) != 0:
        pass
    rename(massage)
