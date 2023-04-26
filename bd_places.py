import sqlite3


# connection = sqlite3.connect('places1.db')
#
# connection.execute('''CREATE TABLE places (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                            name TEXT NOT NULL,
#                                            coords_x FLOAT NOT NULL,
#                                            coords_y FLOAT NOT NULL);''')
#
# # Вставка данных в таблицу
# connection.execute("INSERT INTO places (name, coords_x, coords_y) VALUES (?, ?, ?)", ('Туса Глебовича', 55.589356, 37.886205))
# connection.execute("INSERT INTO places (name, coords_x, coords_y) VALUES (?, ?, ?)", ('Туса Сергеевича', 55.746436, 38.009049))
#
# # Сохранение изменений
# connection.commit()
#
# connection.close()

def nearest(lon, lat):
    connection = sqlite3.connect('places1.db')
    # Извлечение данных из таблицы
    cursor = connection.execute("SELECT * FROM places")
    min=1000000
    n_row='не нашел'
    for row in cursor:
        d = (((row[2]) - lat) ** 2 + ((row[3]) - lon) ** 2) ** 0.5
        if d<min:
            min=d
            n_row=row[1]
    return n_row



