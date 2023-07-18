import sqlite3
from db import posts
from config import DIRECTORY

directory = r'{0}\users.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cur = connection.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, 
        iter INTEGER NOT NULL, state_name TEXT NOT NULL, lon REAL, lat REAL, sorted_distance TEXT);''')  # поменять name NOT NULL
connection.commit()
cur.close()


def insert(user_id, name="-"):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO users(id, name, iter, state_name, lon, lat) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, 0, 'start', 0, 0))
    connection.commit()
    cur.close()


def is_exist(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.commit()
    cur.close()
    if result is not None:
        return True
    else:
        return False


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
    sorted_dist = posts.nearest(lon, lat)
    cur.execute("UPDATE users SET lon = ?, lat = ?, sorted_distance = ? WHERE id = ?", (lon, lat, sorted_dist, user_id))
    connection.commit()
    cur.close()


def fetch_sorted_dist(user_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT sorted_distance FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.commit()
    cur.close()
    return data[0]
