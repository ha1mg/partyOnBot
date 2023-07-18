import sqlite3
from config import DIRECTORY

directory = r'{0}\top.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS top (id_post INTEGER NOT NULL);''')

connection.commit()
cursor.close()
connection.close()

def fetch():
    con = sqlite3.connect(directory)
    cur = con.cursor()
    data = cur.execute("SELECT id_post FROM top").fetchall()
    cur.close()
    con.close()
    return data
