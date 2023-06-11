import sqlite3

connection = sqlite3.connect('users.db')
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXIST users (id INT NOT NULL PRIMARY KEY, name TEXT NOT NULL);''')

connection.commit()
cur.close()

def insert(id, name = "-"):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO users (id, name) VALUES (?, ?)", (id, name))
    connection.commit()
    cur.close()

def isExist(id_user):
    connection = sqlite3.connect('favourite.db')
    cur = connection.cursor()
    if cur.fetchone(id_user):
        return True
    else:
        return False
    connection.commit()
    cur.close()

