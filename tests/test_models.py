from datetime import date

import pytest

from models import FilmReviewSystem, Movie, Review, User


def test_movie_average_rating() -> None:
    movie = Movie(
        movie_id=1,
        title="Interstellar",
        year=2014,
        genre="Sci-Fi",
        director="Christopher Nolan",
    )
    first_user = User(1, "Alex")
    second_user = User(2, "Marina")
    movie.reviews = [
        Review(1, movie, first_user, 10, "Excellent"),
        Review(2, movie, second_user, 8, "Good"),
    ]

    assert movie.average_rating == 9.0


def test_review_rating_validation() -> None:
    movie = Movie(1, "Interstellar", 2014, "Sci-Fi", "Christopher Nolan")
    user = User(1, "Alex")

    with pytest.raises(ValueError):
        Review(1, movie, user, 11, "Invalid rating")


def test_review_links_movie_and_user_instances() -> None:
    movie = Movie(1, "Matrix", 1999, "Sci-Fi", "Wachowski")
    user = User(1, "Alex", date(2026, 9, 22))
    review = Review(1, movie, user, 9, "Strong film")

    assert review.movie is movie
    assert review.user is user
    assert review.movie_id == movie.movie_id
    assert review.user_id == user.user_id


def test_system_add_review_links_movie_and_user() -> None:
    movie = Movie(1, "Matrix", 1999, "Sci-Fi", "Wachowski")
    user = User(1, "Alex", date(2026, 9, 22))
    system = FilmReviewSystem(movies=[movie], users=[user])

    review = system.add_review(movie, user, 9, "Strong film")

    assert review in system.reviews
    assert review in system.get_movie(1).reviews
    assert review.movie is movie
    assert review.user is user
