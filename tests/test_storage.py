from pathlib import Path

from models import FilmReviewSystem, Movie, Review, User
from storage import load_system, save_system


def test_save_and_load_system(tmp_path: Path) -> None:
    movies_file = tmp_path / "movies.json"
    users_file = tmp_path / "users.json"
    reviews_file = tmp_path / "reviews.json"
    movie = Movie(1, "Interstellar", 2014, "Sci-Fi", "Nolan")
    user = User(1, "Alex")
    review = Review(1, movie, user, 10, "Excellent")
    system = FilmReviewSystem(
        movies=[movie],
        users=[user],
        reviews=[review],
    )

    save_system(system, movies_file, users_file, reviews_file)
    loaded = load_system(movies_file, users_file, reviews_file)

    assert loaded.movies[0].title == "Interstellar"
    assert loaded.users[0].name == "Alex"
    assert loaded.movies[0].average_rating == 10.0
    assert loaded.reviews[0].movie is loaded.movies[0]
    assert loaded.reviews[0].user is loaded.users[0]
