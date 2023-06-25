import sqlite3

directory = r'D:\PyProjects\aiogramBot\db\posts.db'
connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT,organization TEXT NOT NULL,
                                    discription TEXT NOT NULL,address TEXT NOT NULL,lat FLOAT NOT NULL,lon FLOAT NOT NULL,date TEXT, media BLOB);''')
# cur.execute("INSERT INTO posts (organization, discription, coords_x, coords_y) VALUES (?, ?, ?, ?)",
#             ('Туса Глебовича',"Будет много Водки", 55.589356, 37.886205))
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

media_post_1 = convertToBinaryData(r'D:\PyProjects\aiogramBot\media\глеб1.jpg')
media_post_2 = convertToBinaryData(r'D:\PyProjects\aiogramBot\media\сергей1.jpg')
media_post_3 = convertToBinaryData(r'D:\PyProjects\aiogramBot\media\вова1.jpg')
#cur.execute("INSERT INTO posts (organization,discription,address,lat,lon,date,media) VALUES (?, ?, ?, ?, ?, ?, ?)",
#('Туса Глебовича',"Будет много Водки","Московская область, Лыткарино, микрорайон 4А, 3",55.589356,37.886205,"25.06.2023", media_post_1))
cur.execute("INSERT INTO posts (organization,discription,address,lat,lon,date,media) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Туса Глебовича',"Будет много Водки","Московская область, Лыткарино, микрорайон 4А, 3",55.589356,37.886205,"25.06.2023", media_post_1))
cur.execute("INSERT INTO posts (organization,discription,address,lat,lon,date,media) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Железнодорожный Party',"Вкусная еда, расстроенная гитара и выход на крышу (вход тоже через неё)","МО, Балашиха, мкр. Саввино, ул. Калинина, 8",55.746436,38.009049,"26.06.2023", media_post_2))
cur.execute("INSERT INTO posts (organization,discription,address,lat,lon,date,media) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Туса у Вовы',"Невероятная возможность оказаться в самом горячем и по-настоящему ядерном месте в России","Кремль",55.751426,37.618879,"31.12.2023", media_post_3))

connection.commit()
cur.close()

# def insertBLOB(post, photo):
#     try:
#
#         sqliteConnection = sqlite3.connect('posts.db')
#         cur = sqliteConnection.cursor()
#         sqlite_insert_blob_query = """ INSERT INTO posts
#                                       (id, media) VALUES (?, ?)"""
#         post_photo = convertToBinaryData(photo)
#         data_tuple = (post, post_photo)
#         cur.execute(sqlite_insert_blob_query, data_tuple)
#         sqliteConnection.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print("Failed to insert blob data into sqlite table", error)
#
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")

def insert(organization, discription, x, y):
    connection = sqlite3.connect(directory)
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (organization, discription, lat, lon) VALUES (?, ?, ?, ?)",
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
    data = cur.execute("SELECT id, lat, lon FROM posts").fetchall()
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