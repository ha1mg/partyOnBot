import sqlite3

connection = sqlite3.connect('top.db')
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXIST top (id_post INT NOT NULL);''')

connection.commit()
cur.close()

def fetch():
    connection = sqlite3.connect()
    cur = connection.cursor()
    cur.execute("SELECT * FROM top")
    data = cur.fetchmany(cur.arraysize)
    connection.commit()
    cur.close()
    return data
