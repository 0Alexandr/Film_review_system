from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one


MOVIE_LIST_SQL = """
    SELECT
        movies.id,
        movies.title,
        movies.year,
        movies.genre,
        movies.director,
        COUNT(reviews.id) AS reviews_count,
        ROUND(AVG(reviews.rating), 1) AS average_rating
    FROM movies
    LEFT JOIN reviews ON reviews.movie_id = movies.id
    GROUP BY movies.id
    ORDER BY average_rating IS NULL, average_rating DESC, movies.title
"""

MOVIE_DETAIL_SQL = """
    SELECT
        movies.id,
        movies.title,
        movies.year,
        movies.genre,
        movies.director,
        COUNT(reviews.id) AS reviews_count,
        ROUND(AVG(reviews.rating), 1) AS average_rating
    FROM movies
    LEFT JOIN reviews ON reviews.movie_id = movies.id
    WHERE movies.id = ?
    GROUP BY movies.id
"""

MOVIE_REVIEWS_SQL = """
    SELECT
        reviews.id,
        users.name AS user_name,
        reviews.rating,
        reviews.recommended
    FROM reviews
    JOIN users ON reviews.user_id = users.id
    WHERE reviews.movie_id = ?
    ORDER BY reviews.publication_date DESC
"""

GENRES_SQL = """
    SELECT DISTINCT genre
    FROM movies
    ORDER BY genre
"""

MOVIE_SEARCH_SQL = """
    SELECT
        movies.id,
        movies.title,
        movies.year,
        movies.genre,
        movies.director,
        COUNT(reviews.id) AS reviews_count,
        ROUND(AVG(reviews.rating), 1) AS average_rating
    FROM movies
    LEFT JOIN reviews ON reviews.movie_id = movies.id
    WHERE (? = '' OR movies.genre = ?)
      AND (? = '' OR movies.title LIKE '%' || ? || '%')
    GROUP BY movies.id
    HAVING COALESCE(AVG(reviews.rating), 0) >= ?
    ORDER BY average_rating DESC, movies.title
"""


def parse_rating(value: str | None) -> float:
    """Преобразовать минимальную оценку из формы в число от 0 до 10."""
    try:
        rating = float(value or 0)
    except ValueError:
        return 0.0
    return min(max(rating, 0.0), 10.0)


def movie_list(request: HttpRequest) -> HttpResponse:
    context = {
        "movies": fetch_all(MOVIE_LIST_SQL),
    }
    return render(request, "catalog/movie_list.html", context)


def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = fetch_one(MOVIE_DETAIL_SQL, [movie_id])
    context = {
        "movie": movie,
        "reviews": fetch_all(MOVIE_REVIEWS_SQL, [movie_id]) if movie else [],
    }
    return render(
        request,
        "catalog/movie_detail.html",
        context,
        status=404 if movie is None else 200,
    )


def movie_search(request: HttpRequest) -> HttpResponse:
    genre = request.GET.get("genre", "").strip()
    query = request.GET.get("q", "").strip()
    min_rating = parse_rating(request.GET.get("min_rating"))
    is_submitted = bool(request.GET)

    movies = []
    if is_submitted:
        movies = fetch_all(
            MOVIE_SEARCH_SQL,
            [genre, genre, query, query, min_rating],
        )

    context = {
        "genres": fetch_all(GENRES_SQL),
        "movies": movies,
        "genre": genre,
        "query": query,
        "min_rating": min_rating,
        "is_submitted": is_submitted,
    }
    return render(request, "catalog/movie_search.html", context)
