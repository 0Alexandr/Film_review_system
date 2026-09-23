from __future__ import annotations

import json
from pathlib import Path

from models import FilmReviewSystem, Movie, Review, User


DATA_DIR = Path("data")
MOVIES_FILE = DATA_DIR / "movies.json"
USERS_FILE = DATA_DIR / "users.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"


def load_json(filename: Path) -> list[dict]:
    """Загрузить список словарей из JSON-файла."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        message = f"Файл {filename} содержит некорректный JSON."
        raise ValueError(message) from error

    if not isinstance(data, list):
        raise ValueError(f"Файл {filename} должен содержать список.")
    return data


def save_json(filename: Path, data: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_system(
    movies_file: Path = MOVIES_FILE,
    users_file: Path = USERS_FILE,
    reviews_file: Path = REVIEWS_FILE,
) -> FilmReviewSystem:
    """Загрузить JSON-данные и преобразовать их в объекты."""
    reviews = [Review.from_dict(item) for item in load_json(reviews_file)]
    movies = [
        Movie.from_dict(
            item,
            reviews=[
                review
                for review in reviews
                if review.movie_id == int(item["movie_id"])
            ],
        )
        for item in load_json(movies_file)
    ]
    users = [User.from_dict(item) for item in load_json(users_file)]
    return FilmReviewSystem(movies=movies, users=users, reviews=reviews)


def save_system(
    system: FilmReviewSystem,
    movies_file: Path = MOVIES_FILE,
    users_file: Path = USERS_FILE,
    reviews_file: Path = REVIEWS_FILE,
) -> None:
    """Сохранить объекты системы в JSON-файлы."""
    save_json(movies_file, [movie.to_dict() for movie in system.movies])
    save_json(users_file, [user.to_dict() for user in system.users])
    save_json(reviews_file, [review.to_dict() for review in system.reviews])
