"""Перенос данных из JSON-файлов проекта в базу SQLite.

Запуск из корня проекта: python -m db.import_json
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from db.database import BASE_DIR, DB_PATH, SCHEMA_FILE, get_connection


DATA_DIR = BASE_DIR / "data"
MOVIES_FILE = DATA_DIR / "movies.json"
USERS_FILE = DATA_DIR / "users.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"


def load_json(filename: Path) -> list[dict]:
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))


def clear_tables(conn: sqlite3.Connection) -> None:
    """Очистить таблицы, чтобы импорт можно было запускать повторно."""
    conn.execute("DELETE FROM reviews")
    conn.execute("DELETE FROM movies")
    conn.execute("DELETE FROM users")


def import_movies(conn: sqlite3.Connection, filename: Path) -> int:
    movies = load_json(filename)
    conn.executemany(
        """
        INSERT INTO movies (id, title, year, genre, director)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                movie["movie_id"],
                movie["title"],
                movie["year"],
                movie["genre"],
                movie.get("director") or None,
            )
            for movie in movies
        ],
    )
    return len(movies)


def import_users(conn: sqlite3.Connection, filename: Path) -> int:
    users = load_json(filename)
    conn.executemany(
        """
        INSERT INTO users (id, name, registration_date)
        VALUES (?, ?, ?)
        """,
        [
            (user["user_id"], user["name"], user["registration_date"])
            for user in users
        ],
    )
    return len(users)


def import_reviews(conn: sqlite3.Connection, filename: Path) -> int:
    reviews = load_json(filename)
    conn.executemany(
        """
        INSERT INTO reviews (
            id, movie_id, user_id, rating, text,
            publication_date, recommended
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                review["review_id"],
                review["movie_id"],
                review["user_id"],
                review["rating"],
                review.get("text") or None,
                review["publication_date"],
                int(review["recommended"]),
            )
            for review in reviews
        ],
    )
    return len(reviews)


def import_all(
    db_path: Path | str = DB_PATH,
    movies_file: Path = MOVIES_FILE,
    users_file: Path = USERS_FILE,
    reviews_file: Path = REVIEWS_FILE,
) -> dict[str, int]:
    """Создать схему и перенести данные; при ошибке откатить изменения."""
    conn = get_connection(db_path)
    try:
        create_schema(conn)
        clear_tables(conn)
        # Сначала родительские таблицы, затем reviews с внешними ключами.
        counts = {
            "movies": import_movies(conn, movies_file),
            "users": import_users(conn, users_file),
            "reviews": import_reviews(conn, reviews_file),
        }
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return counts


def main() -> None:
    counts = import_all()
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
