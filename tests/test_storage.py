from pathlib import Path

from models import FilmReviewSystem, Movie, Review, User
from storage import load_system, save_system


def test_save_and_load_system(tmp_path: Path) -> None:
    movies_file = tmp_path / "movies.json"
    users_file = tmp_path / "users.json"
    reviews_file = tmp_path / "reviews.json"
    system = FilmReviewSystem(
        movies=[Movie(1, "Интерстеллар", 2014, "Фантастика", "Нолан")],
        users=[User(1, "Алексей")],
        reviews=[Review(1, 1, 1, 10, "Отлично")],
    )

    save_system(system, movies_file, users_file, reviews_file)
    loaded = load_system(movies_file, users_file, reviews_file)

    assert loaded.movies[0].title == "Интерстеллар"
    assert loaded.users[0].name == "Алексей"
    assert loaded.movies[0].average_rating == 10.0
