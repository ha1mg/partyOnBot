import sqlite3

connection = sqlite3.connect('top.db')
cur = connection.cursor()
try:
    cur.execute("SELECT * FROM top")
    data = cur.fetchall()
    print("БД top уже существует")
except:
    cur.execute('''CREATE TABLE top (id_post INT NOT NULL);''')
    print("БД top создана")

connection.commit()
cur.close()