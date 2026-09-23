from __future__ import annotations

import json
from pathlib import Path

from models import FilmReviewSystem, Movie, Review, User


DATA_DIR = Path("data")
MOVIES_FILE = DATA_DIR / "movies.json"
USERS_FILE = DATA_DIR / "users.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"


def load_json(filename: Path) -> list[dict]:
    """Load a list of dictionaries from a JSON file."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        message = f"File {filename} contains invalid JSON."
        raise ValueError(message) from error

    if not isinstance(data, list):
        raise ValueError(f"File {filename} must contain a list.")
    return data


def save_json(filename: Path, data: list[dict]) -> None:
    """Save a list of dictionaries to a JSON file."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_system(
    movies_file: Path = MOVIES_FILE,
    users_file: Path = USERS_FILE,
    reviews_file: Path = REVIEWS_FILE,
) -> FilmReviewSystem:
    """Load JSON data and convert it into connected model objects."""
    users = [User.from_dict(item) for item in load_json(users_file)]
    movies = [Movie.from_dict(item) for item in load_json(movies_file)]
    movies_by_id = {movie.movie_id: movie for movie in movies}
    users_by_id = {user.user_id: user for user in users}
    reviews = []

    for item in load_json(reviews_file):
        movie_id = int(item["movie_id"])
        user_id = int(item["user_id"])
        if movie_id not in movies_by_id:
            raise ValueError(f"Movie id={movie_id} for review not found.")
        if user_id not in users_by_id:
            raise ValueError(f"User id={user_id} for review not found.")
        reviews.append(
            Review.from_dict(
                item,
                movie=movies_by_id[movie_id],
                user=users_by_id[user_id],
            )
        )

    return FilmReviewSystem(movies=movies, users=users, reviews=reviews)


def save_system(
    system: FilmReviewSystem,
    movies_file: Path = MOVIES_FILE,
    users_file: Path = USERS_FILE,
    reviews_file: Path = REVIEWS_FILE,
) -> None:
    """Save system objects to JSON files."""
    save_json(movies_file, [movie.to_dict() for movie in system.movies])
    save_json(users_file, [user.to_dict() for user in system.users])
    save_json(reviews_file, [review.to_dict() for review in system.reviews])
