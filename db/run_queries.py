"""Выполнить все запросы из sql/queries.sql и вывести результаты.

Запуск из корня проекта: python -m db.run_queries
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from db.database import BASE_DIR, get_connection


QUERIES_FILE = BASE_DIR / "sql" / "queries.sql"


def split_queries(filename: Path = QUERIES_FILE) -> list[tuple[str, str]]:
    """Разбить файл на пары (комментарий-заголовок, текст запроса)."""
    queries = []
    title = ""
    buffer: list[str] = []
    for line in filename.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        is_title = stripped.startswith("-- ") and stripped[3:4].isdigit()
        if not buffer and is_title:
            title = stripped[3:]
            continue
        if stripped.startswith("--") and not buffer:
            continue
        if stripped or buffer:
            buffer.append(line)
        statement = "\n".join(buffer)
        if buffer and sqlite3.complete_statement(statement):
            queries.append((title, statement.strip()))
            buffer = []
    return queries


def main() -> None:
    conn = get_connection()
    try:
        for title, sql in split_queries():
            cursor = conn.execute(sql)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            print(f"\n== {title}")
            print(" | ".join(columns))
            for row in rows:
                print(" | ".join(str(value) for value in row))
            print(f"({len(rows)} строк)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
