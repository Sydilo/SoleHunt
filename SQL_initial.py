import sqlite3

conn = sqlite3.connect('sneakers.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        user_rating INTEGER,
        user_league TEXT,
        user_last_button_press_timer INTEGER
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS sneakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        image TEXT,
        type TEXT,
        rarity TEXT,
        price INTEGER,
        heat INTEGER
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS user_sneakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        related_user INTEGER,
        related_sneaker INTEGER,
        FOREIGN KEY (related_user) REFERENCES users(user_id),
        FOREIGN KEY (related_sneaker) REFERENCES sneakers(id)
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS promo_sneakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        promo_code TEXT,
        related_sneaker INTEGER,
        FOREIGN KEY (related_sneaker) REFERENCES sneakers(id)
    );
''')


conn.commit()
conn.close()
