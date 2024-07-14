import sqlite3
import pandas as pd
import os

class DbOperator():
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def show_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return tables

    def join_tables(self, table1, table2, key1, key2):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table1} JOIN {table2} ON {table1}.{key1} = {table2}.{key2}")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        rows.insert(0, column_names)
        return rows

    def __del__(self):
        print("close db connection")
        self.conn.close()


if __name__ == '__main__':
    dir_current = os.path.dirname(__file__)
    db = DbOperator(dir_current + "/chinook.db")
    print(db.db_path)
    datas = db.join_tables("albums", "artists", "ArtistId", "ArtistId")
    datas = pd.DataFrame(datas)
    datas.columns = datas.iloc[0]
    datas = datas.drop(0)
    print(datas.head())
