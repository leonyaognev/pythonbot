import sqlite3

DB_FILE_PATH = 'database/data.db'


def create_tables():
    con = sqlite3.connect(DB_FILE_PATH)
    sql = '''
        create table if not exists chanels (
            id integer primary key,
            chanelname text unique,
            linkchanel text integer
            )
    '''
    con.execute(sql)

    con.commit()


class Chanel:
    def __init__(self, id, chanelname, linkchanel):
        self.id = id
        self.chanelname = chanelname
        self.linkchanel = linkchanel


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

    def get_link_by_id(self, id):
        SQL_SELECT = "SELECT linkchanel FROM chanels WHERE id = ?"
        con = sqlite3.connect(DB_FILE_PATH)
        query = con.execute(SQL_SELECT, [id])
        file_data = query.fetchone()
        print(file_data)
        if file_data:
            return file_data[0]
        return None

    def update_link(self, id, channel_id):
        print(id, channel_id)
        SQL = f"UPDATE chanels SET linkchanel = {
            id} WHERE id = {channel_id}"
        con = sqlite3.connect(DB_FILE_PATH)
        con.execute(SQL)
        con.commit()
