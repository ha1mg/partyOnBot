import sqlite3
from config import DIRECTORY

directory = r'{0}\favourite.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS favourite (organization TEXT NOT NULL, user_id INTEGER NOT NULL);''')
connection.commit()

cursor.close()
connection.close()


def insert(organization, id_user):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("INSERT INTO favourite (organization, user_id) VALUES (?, ?)", (organization, id_user))
    con.commit()

    cur.close()
    con.close()


def fetch(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT organization FROM favourite WHERE user_id = ?", (user_id,)).fetchall()

    cur.close()
    con.close()

    return data


def is_exist(org, user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    result = cur.execute("SELECT * FROM favourite WHERE organization = ? AND user_id = ?", (org, user_id))

    cur.close()
    con.close()

    if result is not None:
        return True
    else:
        return False
