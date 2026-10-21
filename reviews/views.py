from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one


REVIEW_LIST_SQL = """
    SELECT
        reviews.id,
        movies.id AS movie_id,
        movies.title AS movie_title,
        movies.genre,
        users.name AS user_name,
        reviews.rating,
        reviews.text,
        reviews.recommended,
        strftime('%d.%m.%Y', reviews.publication_date) AS publication_date
    FROM reviews
    JOIN movies ON reviews.movie_id = movies.id
    JOIN users ON reviews.user_id = users.id
    WHERE (? = '' OR reviews.recommended = ?)
    ORDER BY reviews.publication_date DESC, reviews.id DESC
"""

REVIEW_DETAIL_SQL = """
    SELECT
        reviews.id,
        movies.id AS movie_id,
        movies.title AS movie_title,
        movies.genre,
        users.name AS user_name,
        reviews.rating,
        reviews.text,
        reviews.recommended,
        strftime('%d.%m.%Y', reviews.publication_date) AS publication_date
    FROM reviews
    JOIN movies ON reviews.movie_id = movies.id
    JOIN users ON reviews.user_id = users.id
    WHERE reviews.id = ?
"""

TOTALS_SQL = """
    SELECT
        COUNT(*) AS reviews_count,
        ROUND(AVG(rating), 1) AS average_rating,
        MIN(rating) AS min_rating,
        MAX(rating) AS max_rating,
        SUM(recommended) AS recommended_count
    FROM reviews
"""

GENRE_STATISTICS_SQL = """
    SELECT
        movies.genre,
        COUNT(DISTINCT movies.id) AS movies_count,
        COUNT(reviews.id) AS reviews_count,
        ROUND(AVG(reviews.rating), 1) AS average_rating
    FROM movies
    LEFT JOIN reviews ON reviews.movie_id = movies.id
    GROUP BY movies.genre
    ORDER BY movies_count DESC, movies.genre
"""

USER_STATISTICS_SQL = """
    SELECT
        users.name AS user_name,
        COUNT(reviews.id) AS reviews_count,
        ROUND(AVG(reviews.rating), 1) AS average_rating,
        SUM(reviews.recommended) AS recommended_count
    FROM users
    LEFT JOIN reviews ON reviews.user_id = users.id
    GROUP BY users.id
    ORDER BY reviews_count DESC, users.name
"""

POPULAR_MOVIES_SQL = """
    SELECT
        movies.id,
        movies.title,
        COUNT(reviews.id) AS reviews_count,
        ROUND(AVG(reviews.rating), 1) AS average_rating
    FROM movies
    JOIN reviews ON reviews.movie_id = movies.id
    GROUP BY movies.id
    HAVING COUNT(reviews.id) >= ?
    ORDER BY average_rating DESC
"""

VERDICT_FILTERS = {"": "Все", "1": "Рекомендуют", "0": "Не рекомендуют"}


def parse_min_reviews(value: str | None) -> int:
    """Порог числа отзывов для HAVING: целое число не меньше 1."""
    try:
        return max(int(value or 2), 1)
    except ValueError:
        return 2


def review_list(request: HttpRequest) -> HttpResponse:
    recommended = request.GET.get("recommended", "")
    if recommended not in VERDICT_FILTERS:
        recommended = ""
    context = {
        "reviews": fetch_all(REVIEW_LIST_SQL, [recommended, recommended]),
        "recommended": recommended,
        "verdict_filters": VERDICT_FILTERS,
    }
    return render(request, "reviews/review_list.html", context)


def review_detail(request: HttpRequest, review_id: int) -> HttpResponse:
    review = fetch_one(REVIEW_DETAIL_SQL, [review_id])
    context = {
        "review": review,
    }
    return render(
        request,
        "reviews/review_detail.html",
        context,
        status=404 if review is None else 200,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    min_reviews = parse_min_reviews(request.GET.get("min_reviews"))
    context = {
        "totals": fetch_one(TOTALS_SQL),
        "genres": fetch_all(GENRE_STATISTICS_SQL),
        "users": fetch_all(USER_STATISTICS_SQL),
        "popular_movies": fetch_all(POPULAR_MOVIES_SQL, [min_reviews]),
        "min_reviews": min_reviews,
    }
    return render(request, "reviews/statistics.html", context)
