import sqlite3

directory = r'D:\Projects\aiogramBot\bd\users.db'
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY, name VARCHAR(20) NOT NULL, iter INTEGER NOT NULL, state VARCHAR(20), lon REAL, lat REAL);''')#поменять name NOT NULL

connection.commit()
cur.close()

def insert(id, name = "-"):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO users(id, name, iter) VALUES (?, ?, ?)", (id, name, 0))
    connection.commit()
    cur.close()

def isExist(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if cur.fetchone() != None:
        return True
    else:
        return False
    connection.commit()
    cur.close()

def fetch_iter(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT iter FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.commit()
    cur.close()
    return data[0]

def reset_iter(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("UPDATE users SET iter = 0 WHERE id = ?", (user_id,))
    connection.commit()
    cur.close()

def increment_iter(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("UPDATE users SET iter = iter + 1 WHERE id = ?", (user_id,))
    connection.commit()
    cur.close()