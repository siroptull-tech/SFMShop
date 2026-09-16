-- Инициализация БД SFMShop:

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);



INSERT INTO users (name, email) VALUES
    ('Иван', 'ivan@test.ru'),
    ('Мария', 'maria@test.ru'),
    ('Петр', 'petr@test.ru');

INSERT INTO products (name, price, quantity) VALUES
    ('Ноутбук', 50000.00, 10),
    ('Мышь', 1500.00, 20),
    ('Клавиатура', 3000.00, 15),
    ('Монитор', 25000.00, 8),
    ('Коврик', 800.00, 30);

INSERT INTO orders (user_id, total) VALUES (1, 53000.00);
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
    (1, 1, 1, 50000.00),
    (1, 2, 2, 1500.00);

INSERT INTO orders (user_id, total) VALUES (2, 3000.00);
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
    (2, 3, 1, 3000.00);
