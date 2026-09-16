
def get_orders_with_products(conn, user_id):
    """Получить заказы пользователя с товарами"""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT o.id, p.name, oi.quantity, p.price
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.id, oi.id
        """,
        (user_id,),
    )
    return cur.fetchall()

def get_user_order_stats(conn):
    """Количество и сумма заказов по каждому пользователю, по убыванию суммы"""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT user_id, COUNT(*), SUM(total)
        FROM orders
        GROUP BY user_id
        ORDER BY SUM(total) DESC
        """
    )
    return cur.fetchall()

def get_user_order_history(conn, user_id):
    """История заказов пользователя с товарами, от новых заказов к старым"""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT o.id, p.name, oi.quantity, o.created_at
        FROM orders o
        INNER JOIN order_items oi ON oi.order_id = o.id
        INNER JOIN products p ON p.id = oi.product_id
        WHERE o.user_id = %s
        ORDER BY o.created_at DESC
        """,
        (user_id,),
    )
    return cur.fetchall()

def get_order_statistics(conn):
    """Статистика по пользователям: id, имя, число заказов, общая сумма"""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT u.id, u.name, COUNT(o.id), SUM(o.total)
        FROM users u
        JOIN orders o ON o.user_id = u.id
        GROUP BY u.id, u.name
        ORDER BY SUM(o.total) DESC
        """
    )
    return cur.fetchall()

def get_top_products(conn, limit=5):
    """Топ товаров по количеству проданных штук"""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.name, SUM(oi.quantity)
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        GROUP BY p.id, p.name
        ORDER BY SUM(oi.quantity) DESC
        LIMIT %s
        """,
        (limit,),
    )
    return cur.fetchall()

if __name__ == "__main__":
    from connection import connect_to_db

    conn = connect_to_db()
    try:
        print(get_orders_with_products(conn, 1))
        print(get_user_order_stats(conn))
        print(get_user_order_history(conn, 1))
        print(get_order_statistics(conn))
        print(get_top_products(conn, limit=5))
    finally:
        conn.close()
