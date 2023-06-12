import sqlite3

directory = r'D:\Projects\aiogramBot\bd\posts.db'
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT,organization TEXT NOT NULL,
                                    discription TEXT NOT NULL, coords_x FLOAT NOT NULL,coords_y FLOAT NOT NULL);''')
# cur.execute("INSERT INTO posts (organization, discription, coords_x, coords_y) VALUES (?, ?, ?, ?)",
#             ('Туса Глебовича',"Будет много Водки", 55.589356, 37.886205))
# cur.execute("INSERT INTO posts (organization, discription, coords_x, coords_y) VALUES (?, ?, ?, ?)",
#             ('Туса Сергеевича',"Вкусная еда, расстроенная гитара и выход на крышу (вход тоже через неё)",
#              55.746436, 38.009049))
# cur.execute("INSERT INTO posts (organization, discription, coords_x, coords_y) VALUES (?, ?, ?, ?)",
#             ('Туса у Вовы',"Невероятная возможность оказаться в самом горячем и понастоящему ядерном месте в России",
#              55.751426, 37.618879))

connection.commit()
cur.close()

def insert(organization, discription, x, y):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (organization, discription, coords_x, coords_y) VALUES (?, ?, ?, ?)",
                (organization, discription, x, y))
    connection.commit()
    cur.close()

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
    data = cur.execute("SELECT id, coords_x, coords_y FROM posts").fetchall()
    data_dist = []
    for row in data:
        distance = (((row[1]) - lat) ** 2 + ((row[2]) - lon) ** 2) ** 0.5
        data_dist.append([row[0], distance])
    sorted_dist = sorted(data_dist, key=lambda data: data[1])
    return ','.join(str(item[0]) for item in sorted_dist) #В этом коде мы проходим по каждому элементу списка my_list и преобразуем его в строку с помощью str(item[0]). Затем мы используем метод join для объединения всех строк в одну строку, разделяя их запятой (',').
    connection.commit()
    cur.close()

def size():
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    return len(cur.execute("SELECT * FROM posts").fetchall())
    connection.commit()
    cur.close()