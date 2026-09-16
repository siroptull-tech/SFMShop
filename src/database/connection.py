import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "sfmshop",
    "user": "sfmshop",
    "password": "sfmshop_pass",
}


def connect_to_db():
    return psycopg2.connect(**DB_CONFIG)

def add_product(conn, product_id, name, price, quantity):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (%s, %s, %s, %s)",
        (product_id, name, price, quantity),
    )
    conn.commit()
    print(f"Товар добавлен: {name}, {price:.2f}, {quantity}")

def get_all_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, quantity FROM products ORDER BY id")
    print("Все товары:")
    for product_id, name, price, quantity in cur.fetchall():
        print(f"({product_id}, '{name}', {price:.2f}, {quantity})")

def update_price(conn, product_id, new_price):
    cur = conn.cursor()
    cur.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, product_id))
    conn.commit()
    print(f"Цена обновлена: {new_price:.2f}")

def create_user(conn, name, email):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
            (name, email),
        )
        user_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return None
    print(f"Пользователь создан: {name}, {email}")
    return user_id

def get_user_by_id(conn, user_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
    except psycopg2.Error as e:
        print(f"Ошибка при поиске пользователя: {e}")
        return None
    if row is None:
        return None
    user = {"id": row[0], "name": row[1], "email": row[2]}
    print(f"Пользователь найден: {user}")
    return user

def create_order(conn, user_id, total):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id",
            (user_id, total),
        )
        order_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при создании заказа: {e}")
        return None
    print(f"Заказ создан: user_id={user_id}, total={total}")
    return order_id

def get_user_orders(conn, user_id):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, user_id, total FROM orders WHERE user_id = %s",
            (user_id,),
        )
        orders = cur.fetchall()
    except psycopg2.Error as e:
        print(f"Ошибка при получении заказов: {e}")
        return None
    print(f"Заказы пользователя: {orders}")
    return orders

def count_products(conn):
    """Сколько всего товаров - агрегат COUNT(*), а не len() по всей таблице."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM products")
        return cur.fetchone()[0]


def get_products_page(conn, limit, offset):
    """Одна страница товаров - LIMIT/OFFSET сразу в SQL."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, price, quantity FROM products ORDER BY id LIMIT %s OFFSET %s",
            (limit, offset),
        )
        return cur.fetchall()


def get_product_by_id(conn, product_id):
    """Один товар по id - фильтр WHERE, без перебора всей таблицы."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, price, quantity FROM products WHERE id = %s",
            (product_id,),
        )
        return cur.fetchone()


def update_product(conn, product_id, name, price, quantity):
    """Обновить товар по id, вернуть число обновлённых строк (0 = не найден)."""
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE products SET name = %s, price = %s, quantity = %s WHERE id = %s",
            (name, price, quantity, product_id),
        )
        conn.commit()
        return cur.rowcount


def delete_product(conn, product_id):
    """Удалить товар по id, вернуть число удалённых строк (0 = не найден)."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return cur.rowcount


def delete_order(conn, order_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        deleted_count = cur.rowcount
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при удалении заказа: {e}")
        return 0
    print(f"Удалено заказов: {deleted_count}")
    return deleted_count


def main():
    conn = connect_to_db()
    try:
        create_user(conn, "Иван", "ivan@test.ru")
        get_user_by_id(conn, 1)
        create_order(conn, 1, 50000.0)
        get_user_orders(conn, 1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()

