import sqlite3

class SQL:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def executeSql(self, query, params = ()):
        self.cursor.execute(query, params)
        return self.conn.commit()

    def createTable(self, tableName, fields):
        paramsFull = []
        for field in fields:
            fieldName = field["name"]
            fieldParams = field["params"]
            paramsFull.append(f"{fieldName} {fieldParams}")

        paramsFull = ", ".join(paramsFull)
        tableQuery = f"CREATE TABLE {tableName}({paramsFull});"
        return self.executeSql(tableQuery)

    def fetch(self, query, params = (), is_many = False):
        self.executeSql(query, params)
        if is_many:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def table_exists(self, table_name):
        return self.fetch("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (table_name,))[0] == 1






