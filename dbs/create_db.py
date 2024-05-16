import os
import sqlite3 as sql


def create_db(path: str):
    connection = sql.connect(os.path.join(path, 'realty.db'))
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE "offers" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        offer_id INTEGER,
        date TEXT,
        price INTEGER,
        adress TEXT,
        area FLOAT,
        rooms TEXT,
        floor INTEGER,
        total_floor INTEGER,
        location_link TEXT,
        user_id INTEGER
        )
    """)
    connection.close()


if __name__ == '__main__':
    create_db('')
