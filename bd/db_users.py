import sqlite3
from bd import db_posts

directory = r'D:\Projects\aiogramBot\bd\users.db'
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, iter INTEGER NOT NULL, state_name TEXT NOT NULL, lon REAL, lat REAL);''')#поменять name NOT NULL

connection.commit()
cur.close()

def insert(id, name = "-"):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO users(id, name, iter, state_name, lon, lat) VALUES (?, ?, ?, ?, ?, ?)", (id, name, 0, 'start', 0, 0))
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

def fetch_state(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT state_name FROM users WHERE id = ?", (user_id,)).fetchone()
    print(data)
    connection.commit()
    cur.close()
    return data[0]

def edit_state(new_state, user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("UPDATE users SET state_name = ? WHERE id = ?", (new_state, user_id))
    connection.commit()
    cur.close()

def recording_coords(lon, lat, user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("UPDATE users SET lon = ?, lat = ? WHERE id = ?", (lon, lat, user_id))
    sorted_dist = db_posts.nearest(lon, lat)
    return(sorted_dist)
    connection.commit()
    cur.close()
