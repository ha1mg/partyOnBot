import sqlite3

connection = sqlite3.connect('top.db')
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXIST top (id_post INT NOT NULL);''')

connection.commit()
cur.close()