from models import Movie, Review


def find_movies(movies: list[Movie], query: str) -> list[Movie]:
    """Найти фильмы по части названия, жанра или имени режиссера."""
    normalized_query = query.lower()
    return [
        movie
        for movie in movies
        if normalized_query in movie.title.lower()
        or normalized_query in movie.genre.lower()
        or normalized_query in movie.director.lower()
    ]


def filter_movies_by_genre(movies: list[Movie], genre: str) -> list[Movie]:
    """Отобрать фильмы указанного жанра."""
    return [movie for movie in movies if movie.has_genre(genre)]


def sort_movies_by_rating(movies: list[Movie]) -> list[Movie]:
    """Отсортировать фильмы по среднему рейтингу."""
    return sorted(movies, key=lambda movie: movie.average_rating, reverse=True)


def get_top_movies(movies: list[Movie], limit: int = 3) -> list[Movie]:
    """Получить несколько лучших фильмов по рейтингу."""
    return sort_movies_by_rating(movies)[:limit]


def get_latest_reviews(reviews: list[Review], limit: int = 5) -> list[Review]:
    """Получить последние добавленные отзывы."""
    return sorted(
        reviews,
        key=lambda review: review.publication_date,
        reverse=True,
    )[:limit]


def get_genre_statistics(movies: list[Movie]) -> dict[str, int]:
    """Посчитать количество фильмов по жанрам."""
    statistics: dict[str, int] = {}
    for movie in movies:
        statistics[movie.genre] = statistics.get(movie.genre, 0) + 1
    return statistics


def get_rating_statistics(movies: list[Movie]) -> dict[str, float]:
    """Посчитать статистику рейтингов по каталогу."""
    rated_movies = [movie for movie in movies if movie.reviews]
    if not rated_movies:
        return {
            "movies": len(movies),
            "rated_movies": 0,
            "average_rating": 0.0,
        }

    rating_sum = sum(movie.average_rating for movie in rated_movies)
    average = rating_sum / len(rated_movies)
    return {
        "movies": len(movies),
        "rated_movies": len(rated_movies),
        "average_rating": round(average, 1),
    }
