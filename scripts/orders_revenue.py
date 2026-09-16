import sqlite3


def connect_to_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup_data(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    cur.executemany(
        "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
        [(1, "Ноутбук", 50000.0), (2, "Мышь", 1500.0)],
    )
    cur.executemany(
        "INSERT INTO orders (id, product_id, quantity) VALUES (?, ?, ?)",
        [(1, 1, 2), (2, 2, 3)],
    )
    conn.commit()


def order_total(conn, order_id):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(p.price * o.quantity)
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.id = ?
        """,
        (order_id,),
    )
    return cur.fetchone()[0]


def total_revenue(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(p.price * o.quantity)
        FROM orders o
        JOIN products p ON o.product_id = p.id
        """
    )
    return cur.fetchone()[0]


def main():
    conn = connect_to_db()
    setup_data(conn)

    cur = conn.cursor()
    cur.execute("SELECT id FROM orders ORDER BY id")
    order_ids = [row[0] for row in cur.fetchall()]

    for order_id in order_ids:
        print(f"Сумма заказа {order_id}: {order_total(conn, order_id)}")

    print(f"Общая выручка: {total_revenue(conn)}")

    conn.close()


if __name__ == "__main__":
    main()
