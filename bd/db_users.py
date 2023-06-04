import sqlite3

connection = sqlite3.connect('users.db')
cur = connection.cursor()
try:
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    print("БД users уже существует")
except:
    cur.execute('''CREATE TABLE users (id INT NOT NULL PRIMARY KEY, name TEXT NOT NULL);''')
    print("БД users создана")

connection.commit()
cur.close()

def insert(id, name = "-"):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO users (id, name) VALUES (?, ?)", (id, name))
    connection.commit()
    cur.close()

def isExist(user_id):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = (?)", (user_id))
    connection.commit()
    cur.close()

