import json
import sqlite3
from pathlib import Path

import pytest

from db.database import get_connection
from db.import_json import MOVIES_FILE, REVIEWS_FILE, USERS_FILE, import_all
from db.run_queries import split_queries


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "test.sqlite"
    import_all(path)
    return path


def count_json(filename: Path) -> int:
    return len(json.loads(filename.read_text(encoding="utf-8")))


def test_schema_creates_tables(db_path: Path) -> None:
    conn = get_connection(db_path)
    tables = {
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    conn.close()

    assert tables == {"movies", "users", "reviews"}


def test_reviews_foreign_keys(db_path: Path) -> None:
    conn = get_connection(db_path)
    foreign_keys = conn.execute("PRAGMA foreign_key_list(reviews)").fetchall()
    conn.close()

    assert {row["table"] for row in foreign_keys} == {"movies", "users"}


def test_import_matches_json(db_path: Path) -> None:
    conn = get_connection(db_path)
    counts = {
        "movies": conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0],
        "users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "reviews": conn.execute("SELECT COUNT(*) FROM reviews").fetchone()[0],
    }
    conn.close()

    assert counts == {
        "movies": count_json(MOVIES_FILE),
        "users": count_json(USERS_FILE),
        "reviews": count_json(REVIEWS_FILE),
    }


def test_import_can_be_repeated(db_path: Path) -> None:
    counts = import_all(db_path)

    assert counts["reviews"] == count_json(REVIEWS_FILE)


def test_foreign_key_is_checked(db_path: Path) -> None:
    conn = get_connection(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO reviews "
            "(id, movie_id, user_id, rating, publication_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (100, 999, 1, 5, "2026-10-01"),
        )
    conn.close()


def test_rating_check_constraint(db_path: Path) -> None:
    conn = get_connection(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO reviews "
            "(id, movie_id, user_id, rating, publication_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (100, 1, 1, 11, "2026-10-01"),
        )
    conn.close()


def test_all_queries_from_file_run(db_path: Path) -> None:
    queries = split_queries()
    conn = get_connection(db_path)
    for title, sql in queries:
        conn.execute(sql).fetchall()
    conn.close()

    assert len(queries) >= 10


def test_rows_are_accessed_by_name(db_path: Path) -> None:
    conn = get_connection(db_path)
    row = conn.execute(
        "SELECT title, year FROM movies WHERE id = ?",
        (1,),
    ).fetchone()
    conn.close()

    assert row["title"] == "Интерстеллар"
    assert row["year"] == 2014
