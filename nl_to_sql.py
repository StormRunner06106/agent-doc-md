import os
import re

from db import DB_PATH


SCHEMA_HINT = """
Tables:
- users(id, name, email, city)
- products(id, name, category, price, stock)
- orders(id, user_id, order_date, status)
- order_items(id, order_id, product_id, quantity)
Only generate read-only SQLite SELECT queries.
"""


EXAMPLES = [
    ("top products", """
        SELECT p.name, SUM(oi.quantity) AS sold
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        GROUP BY p.id, p.name
        ORDER BY sold DESC;
    """),
    ("revenue", """
        SELECT o.id AS order_id, u.name AS customer,
               SUM(oi.quantity * p.price) AS revenue
        FROM orders o
        JOIN users u ON u.id = o.user_id
        JOIN order_items oi ON oi.order_id = o.id
        JOIN products p ON p.id = oi.product_id
        WHERE o.status != 'cancelled'
        GROUP BY o.id, u.name
        ORDER BY revenue DESC;
    """),
    ("users", "SELECT * FROM users;"),
    ("products", "SELECT * FROM products;"),
    ("orders", "SELECT * FROM orders;"),
]


def fallback_sql(prompt: str) -> str:
    text = prompt.lower()
    for key, sql in EXAMPLES:
        if key in text:
            return " ".join(sql.split())
    if "customer" in text or "city" in text:
        return "SELECT id, name, email, city FROM users ORDER BY name;"
    return "SELECT * FROM products LIMIT 20;"


def langchain_sql(prompt: str) -> str | None:
    if not os.getenv("OPENAI_API_KEY"):
        return None

    from langchain_community.utilities import SQLDatabase
    from langchain_openai import ChatOpenAI

    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    message = (
        f"{SCHEMA_HINT}\nQuestion: {prompt}\n"
        "Return only one SQLite SELECT query. No markdown."
    )
    response = llm.invoke(message)
    return response.content.strip()


def to_sql(prompt: str) -> str:
    sql = langchain_sql(prompt) or fallback_sql(prompt)
    return clean_sql(sql)


def clean_sql(sql: str) -> str:
    sql = re.sub(r"```(?:sql)?|```", "", sql, flags=re.IGNORECASE).strip()
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    if ";" in sql[:-1]:
        raise ValueError("Only one query can be executed.")
    return sql.rstrip(";") + ";"
