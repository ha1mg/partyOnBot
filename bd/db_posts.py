import sqlite3

connection = sqlite3.connect('posts.db')
cur = connection.cursor()
try:
    cur.execute("SELECT * FROM posts")
    data = cur.fetchall()
    print("БД places уже существует")
except:
    cur.execute('''CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,
                                               coords_x FLOAT NOT NULL,coords_y FLOAT NOT NULL);''') #IF NOT EXIST
    print("БД places создана")

connection.commit()
cur.close()

# cur.execute("INSERT INTO places (name, coords_x, coords_y) VALUES (?, ?, ?)", ('Туса Глебовича', 55.589356, 37.886205))
# cur.execute("INSERT INTO places (name, coords_x, coords_y) VALUES (?, ?, ?)", ('Туса Сергеевича', 55.746436, 38.009049))

def insert(name, x, y):
    connection = sqlite3.connect('posts.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (name, coords_x, coords_y) VALUES (?, ?, ?)",
                (name, x, y))
    connection.commit()
    cur.close()

def fetch(post_id):
    connection = sqlite3.connect()
    cur = connection.cursor()
    data = cur.execute("SELECT * FROM posts WHERE id = (post_id) VALUES (?)", (post_id))
    connection.commit()
    cur.close()
    return data

# def nearest(lon, lat):
#     connection = sqlite3.connect('posts.db')
#     cur = connection.cursor()
#     data = cur.execute("SELECT * FROM posts")
#
#     min = 1000000
#     n_row = 'не нашел'
#     for row in data:
#         d = (((row[2]) - lat) ** 2 + ((row[3]) - lon) ** 2) ** 0.5
#         if d < min:
#             min = d
#             n_row = row[1]
#     connection.commit()
#     cur.close()
#     return n_row


def nearest(lon, lat):
    connection = sqlite3.connect('posts.db')
    cur = connection.cursor()
    data = tuple(cur.fetchall())

    #картеж с расстояниями
    data_dist = []

    min = 1000000
    n_row = 'не нашел'
    for row in data:
        distance = (((row[2]) - lat) ** 2 + ((row[3]) - lon) ** 2) ** 0.5
        data_dist.append([row[0], distance])

    sorted_dist = sorted(data_dist, key=lambda data: data[1])
    for i in sorted_dist:
        data_dist.pop(1)

    return data_dist

