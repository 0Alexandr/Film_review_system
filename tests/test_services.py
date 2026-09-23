from models import Movie, Review, User
from services import (
    filter_movies_by_genre,
    find_movies,
    get_rating_statistics,
    sort_movies_by_rating,
)


def make_movies() -> list[Movie]:
    user = User(1, "Alex")
    interstellar = Movie(
        1,
        "Interstellar",
        2014,
        "Sci-Fi",
        "Christopher Nolan",
    )
    parasite = Movie(
        2,
        "Parasite",
        2019,
        "Drama",
        "Bong Joon Ho",
    )
    comedy = Movie(3, "Comedy", 2020, "Comedy", "Author")

    interstellar.add_review(Review(1, interstellar, user, 10, "Excellent"))
    parasite.add_review(Review(2, parasite, user, 9, "Strong"))
    return [interstellar, parasite, comedy]


def test_find_movies_by_genre() -> None:
    result = find_movies(make_movies(), "drama")

    assert [movie.title for movie in result] == ["Parasite"]


def test_filter_movies_by_genre() -> None:
    result = filter_movies_by_genre(make_movies(), "Sci-Fi")

    assert len(result) == 1
    assert result[0].title == "Interstellar"


def test_sort_movies_by_rating() -> None:
    result = sort_movies_by_rating(make_movies())

    assert [movie.title for movie in result] == [
        "Interstellar",
        "Parasite",
        "Comedy",
    ]


def test_rating_statistics() -> None:
    statistics = get_rating_statistics(make_movies())

    assert statistics == {
        "movies": 3,
        "rated_movies": 2,
        "average_rating": 9.5,
    }
