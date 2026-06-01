import argparse
import sqlite3
from pathlib import Path

from db import DB_PATH, init_db


def get_tables(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()
    return [row[0] for row in rows]


def print_table(conn: sqlite3.Connection, table: str, limit: int) -> None:
    rows = conn.execute(f'SELECT * FROM "{table}" LIMIT ?', (limit,)).fetchall()
    columns = [column[0] for column in conn.execute(f'SELECT * FROM "{table}" LIMIT 0').description]

    print(f"\n## {table}")
    print(" | ".join(columns))
    print("-" * max(12, len(" | ".join(columns))))

    if not rows:
        print("(no rows)")
        return

    for row in rows:
        print(" | ".join(str(value) for value in row))


def main() -> None:
    parser = argparse.ArgumentParser(description="Print rows from the eshop SQLite database.")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="Path to the .db file.")
    parser.add_argument("--limit", type=int, default=20, help="Rows to show per table.")
    args = parser.parse_args()

    if args.db == DB_PATH:
        init_db()

    if not args.db.exists():
        raise SystemExit(f"Database not found: {args.db}")

    with sqlite3.connect(args.db) as conn:
        tables = get_tables(conn)
        if not tables:
            raise SystemExit(f"No tables found in {args.db}")

        print(f"Database: {args.db}")
        for table in tables:
            print_table(conn, table, args.limit)


if __name__ == "__main__":
    main()
