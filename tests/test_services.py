from models import Movie, Review
from services import (
    filter_movies_by_genre,
    find_movies,
    get_rating_statistics,
    sort_movies_by_rating,
)


def make_movies() -> list[Movie]:
    return [
        Movie(
            1,
            "Интерстеллар",
            2014,
            "Фантастика",
            "Кристофер Нолан",
            [Review(1, 1, 1, 10, "Отлично")],
        ),
        Movie(
            2,
            "Паразиты",
            2019,
            "Драма",
            "Пон Джун-хо",
            [Review(2, 2, 1, 9, "Сильно")],
        ),
        Movie(3, "Комедия", 2020, "Комедия", "Автор"),
    ]


def test_find_movies_by_genre() -> None:
    result = find_movies(make_movies(), "драма")

    assert [movie.title for movie in result] == ["Паразиты"]


def test_filter_movies_by_genre() -> None:
    result = filter_movies_by_genre(make_movies(), "Фантастика")

    assert len(result) == 1
    assert result[0].title == "Интерстеллар"


def test_sort_movies_by_rating() -> None:
    result = sort_movies_by_rating(make_movies())

    assert [movie.title for movie in result] == [
        "Интерстеллар",
        "Паразиты",
        "Комедия",
    ]


def test_rating_statistics() -> None:
    statistics = get_rating_statistics(make_movies())

    assert statistics == {
        "movies": 3,
        "rated_movies": 2,
        "average_rating": 9.5,
    }
