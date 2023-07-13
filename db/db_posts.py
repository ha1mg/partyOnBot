import sqlite3
from config import DIRECTORY

directory = r'{0}\posts.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,organization TEXT NOT NULL,date TEXT NOT NULL,
            description TEXT NOT NULL,address TEXT NOT NULL,lat FLOAT NOT NULL,lon FLOAT NOT NULL,media_id TEXT);''')

connection.commit()
cur.close()

def insert(organization,date,description,address,lat,lon):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (organization,date,description,address,lat,lon) VALUES (?, ?, ?, ?, ?, ?)",
                (organization, date, description, address, lat, lon))
    connection.commit()
    result = cur.lastrowid
    cur.close()
    return result

def fetch(post_id):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    connection.commit()
    cur.close()
    return data

def fetch_by_organization(org):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT * FROM posts WHERE organization = ?", (org,)).fetchone()
    connection.commit()
    cur.close()
    return data

def nearest(lon, lat):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    data = cur.execute("SELECT id, lat, lon FROM posts").fetchall()
    data_dist = []
    for row in data:
        distance = (((row[1]) - lat) ** 2 + ((row[2]) - lon) ** 2) ** 0.5
        data_dist.append([row[0], distance])
    sorted_dist = sorted(data_dist, key=lambda data: data[1])
    connection.commit()
    cur.close()
    return ','.join(str(item[0]) for item in sorted_dist)  # В этом коде мы проходим по каждому элементу списка my_list и преобразуем его в строку с помощью str(item[0]). Затем мы используем метод join для объединения всех строк в одну строку, разделяя их запятой (',').

def size():
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    connection.commit()
    result = len(cur.execute("SELECT * FROM posts").fetchall())
    cur.close()
    return result

