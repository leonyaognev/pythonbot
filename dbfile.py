import sqlite3
from random import choice

DB_FILE_PATH = 'database/data.db'


def create_tables():
    con = sqlite3.connect(DB_FILE_PATH)
    sql = '''
        create table if not exists chanels (
            id integer primary key,
            chanelname text unique,
            descrchanel text unique,
            linkchanel text unique
            )
    '''
    con.execute(sql)

    con.commit()


class Chanel:
    def __init__(self, id, chanelname, descrchanel, linkchanel):
        self.id = id
        self.chanelname = chanelname
        self.descrchanel = descrchanel
        self.linkchanel = linkchanel


class ChanelService:
    def add(self, file_data):
        SQL_INSERT = """
            INSERT INTO chanels (chanelname, descrchanel, linkchanel)
            VALUES (?, ?, ?)
        """
        if self.get_by_chanelname(file_data):
            return 0

        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        text = [choice(letters) for i in range(16)]

        linkchanel = ''.join(text)
        namechanel = file_data
        descrchanel = 'все серии' + file_data + '''только в нашем канале!!!!\n
            еще больше контента в нашем боте @leognburs'''

        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL_INSERT, [namechanel, descrchanel, linkchanel])
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

    def get_link_by_id(self, id):
        SQL_SELECT = "SELECT linkchanel FROM chanels WHERE id = ?"
        con = sqlite3.connect(DB_FILE_PATH)
        query = con.execute(SQL_SELECT, [id])
        file_data = query.fetchone()
        print(file_data)
        if file_data:
            return file_data[0]
        return None
