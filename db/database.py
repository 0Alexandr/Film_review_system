"""Подключение к базе данных SQLite проекта «КиноОтзыв»."""

from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "filmreviews.sqlite"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Открыть соединение с проверкой внешних ключей и именованными полями."""
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def fetch_all(sql: str, params: tuple | list = ()) -> list[sqlite3.Row]:
    """Выполнить SELECT и вернуть все строки результата."""
    conn = get_connection()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def fetch_one(sql: str, params: tuple | list = ()) -> sqlite3.Row | None:
    """Выполнить SELECT и вернуть первую строку или None."""
    conn = get_connection()
    try:
        return conn.execute(sql, params).fetchone()
    finally:
        conn.close()
