import sqlite3
from config import DIRECTORY

directory = r'{0}\managers.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS managers (
            id INTEGER NOT NULL,name TEXT NOT NULL,organization TEXT NOT NULL);''')
connection.commit()

cursor.close()
connection.close()


def fetch(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT organization FROM managers WHERE id = ?", (user_id,)).fetchall()

    cur.close()
    con.close()

    return [x[0] for x in data]


def fetch_id():
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT id FROM managers").fetchall()

    cur.close()
    con.close()

    return [x[0] for x in data]
