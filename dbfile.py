import sqlite3
import random

DB_FILE_PATH = 'database/data.db'


def create_tables():
    con = sqlite3.connect(DB_FILE_PATH)
    sql = '''
        create table if not exists chanels (
            id integer primary key,
            chanelname text unique,
            linkchanel integer,
            invitelink text,
            file_id text,
            caption text
            )
    '''
    con.execute(sql)

    con.commit()


class Chanel:
    def __init__(self, id, chanelname, linkchanel, invitelink, file_id, caption):
        self.id = id
        self.chanelname = chanelname
        self.linkchanel = linkchanel
        self.invitelink = invitelink
        self.file_id = file_id
        self.caption = caption


class ChanelService:
    def add(self, file_data):
        SQL_INSERT = """
            INSERT INTO chanels (chanelname)
            VALUES (?)
        """
        if self.get_by_chanelname(file_data):
            return 0

        namechanel = file_data

        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL_INSERT, [namechanel])
        con.commit()
        return self.get_by_chanelname(file_data)

    def get_by_chanelname(self, chanelname):
        SQL_SELECT = "SELECT * FROM chanels WHERE chanelname = ?"
        con = sqlite3.connect(DB_FILE_PATH)
        query = con.execute(SQL_SELECT, [chanelname])
        file_data = query.fetchone()
        if file_data:
            return Chanel(*file_data)
        return None

    def get_by_id(self, id):
        SQL_SELECT = "SELECT * FROM chanels WHERE id = ?"
        con = sqlite3.connect(DB_FILE_PATH)
        query = con.execute(SQL_SELECT, [id])
        file_data = query.fetchone()
        if file_data:
            return Chanel(*file_data)
        return None

    def update_link(self, id, channel_id):
        SQL = f"UPDATE chanels SET linkchanel = {
            id} WHERE id = {channel_id}"
        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL)
        con.commit()

    def update_inviteLink(self, link, channel_id):
        SQL = f"UPDATE chanels SET invitelink = '{link}' WHERE id = {
            channel_id}"
        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL)
        con.commit()

    def update_file_id(self, file_id, channel_id):
        SQL = f"UPDATE chanels SET file_id = '{file_id}' WHERE id = {
            channel_id}"
        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL)
        con.commit()

    def random_serial(self):
        con = sqlite3.connect(DB_FILE_PATH)

        qwery = con.execute("SELECT MIN(id), MAX(id) FROM chanels")
        min_id, max_id = qwery.fetchone()

        random_id = random.randint(min_id, max_id)

        qwery = con.execute(
            "SELECT * FROM chanels WHERE id = ?", (random_id,))
        file_data = qwery.fetchone()
        if file_data:
            return Chanel(*file_data)
        return None

    def update_caption(self, caption, channel_id):
        SQL = f"UPDATE chanels SET caption = '{caption}' WHERE id = {
            channel_id}"
        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL)
        con.commit()
