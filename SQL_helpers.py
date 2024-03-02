import sqlite3


class SQLConnector:
    def __init__(self):
        with sqlite3.connect('sneakers.db') as self.connection:
            self.cursor = self.connection.cursor()


class SQLCommandor(SQLConnector):
    def __init__(self):
        super().__init__()

    def sql_select(self, query, params=()):
        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def sql_insert(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def sql_update(self, query, params=()):
        self.sql_insert(query, params)

    def sql_delete(self, query, params=()):
        self.sql_insert(query, params)
