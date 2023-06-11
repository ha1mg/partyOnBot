import sqlite3

connection = sqlite3.connect('favourite.db')
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS favourite (organization INT NOT NULL, user_id INT NOT NULL);''')

connection.commit()
cur.close()

def insert(id_post, id_user):
    connection = sqlite3.connect('favourite.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO favourite (id, name) VALUES (?, ?)", (id_post, id_user))
    connection.commit()
    cur.close()

def fetch(user_id):
    connection = sqlite3.connect()
    cur = connection.cursor()
    cur.execute("SELECT * FROM posts WHERE user_id = (id) VALUES (?)", (user_id))
    data = cur.fetchall()
    for i in data:
        data.pop(2)
    connection.commit()
    cur.close()
    return data