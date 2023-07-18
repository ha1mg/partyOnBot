import sqlite3
from db import posts
from config import DIRECTORY

directory = r'{0}\users.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, 
        iter INTEGER NOT NULL, state_name TEXT NOT NULL, lon REAL, lat REAL, sorted_distance TEXT);''')  
connection.commit()

cursor.close()
connection.close()


def insert(user_id, name="-"):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("INSERT INTO users(id, name, iter, state_name, lon, lat) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, 0, 'start', 0, 0))
    con.commit()

    cur.close()
    con.close()


def is_exist(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    result = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    cur.close()
    con.close()

    if result is not None:
        return True
    else:
        return False


def fetch_iter(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT iter FROM users WHERE id = ?", (user_id,)).fetchone()

    cur.close()
    con.close()

    return data[0]


def reset_iter(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("UPDATE users SET iter = 0 WHERE id = ?", (user_id,))
    con.commit()

    cur.close()
    con.close()


def increment_iter(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("UPDATE users SET iter = iter + 1 WHERE id = ?", (user_id,))
    con.commit()

    cur.close()
    con.close()


def fetch_state(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT state_name FROM users WHERE id = ?", (user_id,)).fetchone()

    cur.close()
    con.close()

    return data[0]


def edit_state(new_state, user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("UPDATE users SET state_name = ? WHERE id = ?", (new_state, user_id))
    con.commit()

    cur.close()
    con.close()


def recording_cords(lon, lat, user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    sorted_dist = posts.nearest(lon, lat)
    cur.execute("UPDATE users SET lon = ?, lat = ?, sorted_distance = ? WHERE id = ?", (lon, lat, sorted_dist, user_id))
    con.commit()

    data = cur.execute("SELECT sorted_distance FROM users WHERE id = ?", (user_id,)).fetchone()

    cur.close()
    con.close()

    return data[0]


def calc_sorted_posts(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()
    
    cords = cur.execute("SELECT lon, lat FROM users WHERE id = ?", (user_id,)).fetchone()
    sorted_dist = posts.nearest(cords[0], cords[1])
    cur.execute("UPDATE users SET sorted_distance = ? WHERE id = ?", (sorted_dist, user_id))
    con.commit()

    data = cur.execute("SELECT sorted_distance FROM users WHERE id = ?", (user_id,)).fetchone()

    cur.close()
    con.close()

    return data[0]


def fetch_sorted_posts(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT sorted_distance FROM users WHERE id = ?", (user_id,)).fetchone()

    cur.close()
    con.close()

    return data[0]

def user_have_location(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT lat FROM users WHERE id = ?", (user_id,)).fetchone()

    if data is not None:
        return True
    else:
        return False

    cur.close()
    con.close()

def take_user_location(user_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT lat, lon FROM users WHERE id = ?", (user_id,)).fetchone()
    resault = data

    cur.close()
    con.close()

    return resault