import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("eshop.db")


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"""


SEED_SQL = """
INSERT INTO users (id, name, email, city) VALUES
    (1, 'Ava Lee', 'ava@example.com', 'New York'),
    (2, 'Noah Kim', 'noah@example.com', 'Seattle'),
    (3, 'Mia Chen', 'mia@example.com', 'Austin'),
    (4, 'Liam Smith', 'liam@example.com', 'Chicago');

INSERT INTO products (id, name, category, price, stock) VALUES
    (1, 'Wireless Mouse', 'Electronics', 24.99, 40),
    (2, 'Mechanical Keyboard', 'Electronics', 89.99, 18),
    (3, 'Coffee Mug', 'Home', 12.50, 75),
    (4, 'Desk Lamp', 'Home', 34.00, 22),
    (5, 'Running Shoes', 'Fashion', 64.99, 12);

INSERT INTO orders (id, user_id, order_date, status) VALUES
    (1, 1, '2026-05-01', 'paid'),
    (2, 1, '2026-05-10', 'shipped'),
    (3, 2, '2026-05-12', 'paid'),
    (4, 3, '2026-05-14', 'cancelled'),
    (5, 4, '2026-05-18', 'paid');

INSERT INTO order_items (id, order_id, product_id, quantity) VALUES
    (1, 1, 1, 2),
    (2, 1, 3, 1),
    (3, 2, 2, 1),
    (4, 3, 5, 1),
    (5, 4, 4, 2),
    (6, 5, 1, 1),
    (7, 5, 4, 1);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA_SQL)
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            conn.executescript(SEED_SQL)
