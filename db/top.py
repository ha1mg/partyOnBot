import sqlite3
from config import DIRECTORY

directory = r'{0}\top.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS top (id_post INTEGER NOT NULL);''')

# cur.execute("INSERT INTO top (id_post) VALUES (?)", (1,))
# cur.execute("INSERT INTO top (id_post) VALUES (?)", (2,))
# cur.execute("INSERT INTO top (id_post) VALUES (?)", (3,))

connection.commit()
cur.close()

def fetch():
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT id_post FROM top").fetchall()
    connection.commit()
    cur.close()
    return data
