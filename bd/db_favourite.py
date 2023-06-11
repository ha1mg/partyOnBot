import sqlite3

directory = r'D:\Projects\aiogramBot\bd\favourite.db'
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS favourite (organization INTEGER NOT NULL, user_id INTEGER NOT NULL);''')

connection.commit()
cur.close()

def insert(id_post, id_user):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO favourite (id, name) VALUES (?, ?)", (id_post, id_user))
    connection.commit()
    cur.close()

def fetch(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("SELECT * FROM posts WHERE user_id = (id) VALUES (?)", (user_id))
    data = cur.fetchall()
    for i in data:
        data.pop(2)
    connection.commit()
    cur.close()
    return data