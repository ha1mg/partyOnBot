import sqlite3

connection = sqlite3.connect('favourite.db')
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXIST favourite (id_post INT NOT NULL, id_user INT NOT NULL);''')

connection.commit()
cur.close()

def insert(id_post, id_user):
    connection = sqlite3.connect('favourite.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO favourite (id, name) VALUES (?, ?)", (id_post, id_user))
    connection.commit()
    cur.close()

def isExist(id_user):
    connection = sqlite3.connect('favourite.db')
    cur = connection.cursor()
    if cur.fetchone(id_user)==None:
        return False
    else:
        return True
    connection.commit()
    cur.close()