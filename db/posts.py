import asyncio
import sqlite3
import schedule
from config import DIRECTORY

directory = r'{0}\posts.db'.format(DIRECTORY)
connection = sqlite3.connect(directory)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,organization TEXT NOT NULL,date TEXT NOT NULL,
            description TEXT NOT NULL,address TEXT NOT NULL,lat FLOAT NOT NULL,lon FLOAT NOT NULL,media_id TEXT);''')

connection.commit()

cursor.close()
connection.close()


def insert(organization, date, description, address, lat, lon):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("INSERT INTO posts (organization,date,description,address,lat,lon) VALUES (?, ?, ?, ?, ?, ?)",
                (organization, date, description, address, lat, lon))
    result = cur.lastrowid

    con.commit()

    cur.close()
    con.close()

    return result


def fetch(post_id):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()

    cur.close()
    con.close()

    return data


def fetch_by_organization(org):
    con = sqlite3.connect(directory)
    cur = con.cursor()

    data = cur.execute("SELECT * FROM posts WHERE organization = ?", (org,)).fetchone()

    cur.close()
    con.close()

    return data


def nearest(lon, lat):
    con = sqlite3.connect(directory)
    cur = con.cursor()
    
    data = cur.execute("SELECT id, date, lat, lon FROM posts ORDER BY date").fetchall()

    cur.close()
    con.close()

    grouped_data_by_date = {}

    for row in data:
        distance = (((row[2]) - lat) ** 2 + ((row[3]) - lon) ** 2) ** 0.5
        if row[1] in grouped_data_by_date:
            grouped_data_by_date[row[1]].append([row[0], distance])
        else:
            grouped_data_by_date[row[1]] = [[row[0], distance]]

    sorted_data = {
        key: sorted(value, key=lambda x: x[1])
        for key, value in grouped_data_by_date.items()
    }
    print(sorted_data)
    result_string = ','.join(str(item[0]) for value in sorted_data.values() for item in value)

    return result_string


def size():
    con = sqlite3.connect(directory)
    cur = con.cursor()

    result = len(cur.execute("SELECT * FROM posts").fetchall())
    
    cur.close()
    con.close()
    
    return result


def delete_posts():
    con = sqlite3.connect(directory)
    cur = con.cursor()

    cur.execute("DELETE FROM posts WHERE date < date('now')")

    con.commit()
    
    cur.close()
    con.close()


# Запускаем задачу удаления ежедневно в определенное время
schedule.every().day.at("00:00").do(delete_posts)


async def schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    schedule()
