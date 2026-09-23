from datetime import date

import pytest

from models import FilmReviewSystem, Movie, Review, User


def test_movie_average_rating() -> None:
    movie = Movie(
        movie_id=1,
        title="Интерстеллар",
        year=2014,
        genre="Фантастика",
        director="Кристофер Нолан",
        reviews=[
            Review(1, 1, 1, 10, "Отлично"),
            Review(2, 1, 2, 8, "Хорошо"),
        ],
    )

    assert movie.average_rating == 9.0


def test_review_rating_validation() -> None:
    with pytest.raises(ValueError):
        Review(1, 1, 1, 11, "Некорректная оценка")


def test_system_add_review_links_movie_and_user() -> None:
    system = FilmReviewSystem(
        movies=[Movie(1, "Матрица", 1999, "Фантастика", "Вачовски")],
        users=[User(1, "Алексей", date(2026, 9, 22))],
    )

    review = system.add_review(1, 1, 9, "Сильный фильм")

    assert review in system.reviews
    assert review in system.get_movie(1).reviews
