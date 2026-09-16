import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        total INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

cur.execute("INSERT INTO users (id, name) VALUES (1, 'Иван')")
cur.execute("INSERT INTO users (id, name) VALUES (2, 'Мария')")

cur.execute("INSERT INTO orders (user_id, total) VALUES (1, 800)")
cur.execute("INSERT INTO orders (user_id, total) VALUES (1, 1200)")
cur.execute("INSERT INTO orders (user_id, total) VALUES (2, 3000)")
conn.commit()

try:
    cur.execute("INSERT INTO orders (user_id, total) VALUES (99, 500)")
    conn.commit()
except sqlite3.IntegrityError:
    print("Заказ для несуществующего пользователя отклонён")

cur.execute("""
    SELECT users.name, SUM(orders.total)
    FROM users
    JOIN orders ON users.id = orders.user_id
    GROUP BY users.id
    ORDER BY SUM(orders.total) DESC
""")

for name, total in cur.fetchall():
    print(f"{name}: {total}")

conn.close()
