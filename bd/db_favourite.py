import sqlite3

directory = r'D:\Projects\aiogramBot\bd\favourite.db'
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
    cur.execute("SELECT * FROM favourite WHERE user_id = ?", (user_id,))
    data = cur.fetchall()
    for i in data:
        data.pop(2)
    connection.commit()
    cur.close()
    return data