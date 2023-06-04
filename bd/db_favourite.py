import sqlite3

connection = sqlite3.connect('favourite.db')
cur = connection.cursor()
try:
    cur.execute("SELECT * FROM favourite")
    data = cur.fetchall()
    print("БД favourite уже существует")
except:
    cur.execute('''CREATE TABLE favourite (id_post INT NOT NULL, id_user INT NOT NULL);''')
    print("БД favourite создана")

connection.commit()
cur.close()

def insert(id_post, id_user):
    connection = sqlite3.connect('favourite.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO favourite (id, name) VALUES (?, ?)", (id_post, id_user))
    connection.commit()
    cur.close()

