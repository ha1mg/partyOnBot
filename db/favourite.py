import sqlite3
from config import DIRECTORY

directory = r'{0}\favourite.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS favourite (organization TEXT NOT NULL, user_id INTEGER NOT NULL);''')

connection.commit()
cur.close()

def insert(organization, id_user):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO favourite (organization, user_id) VALUES (?, ?)", (organization, id_user))
    connection.commit()
    cur.close()

def fetch(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    return cur.execute("SELECT organization FROM favourite WHERE user_id = ?", (user_id,)).fetchall()
    connection.commit()
    cur.close()
    return data

def is_exist(org, user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("SELECT * FROM favourite WHERE organization = ? AND user_id = ?", (org, user_id))
    if cur.fetchone() != None:
        return True
    else:
        return False
    connection.commit()
    cur.close()