from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one


SUMMARY_SQL = """
    SELECT
        (SELECT COUNT(*) FROM movies) AS movies_count,
        (SELECT COUNT(DISTINCT movie_id) FROM reviews) AS rated_movies_count,
        (SELECT ROUND(AVG(rating), 1) FROM reviews) AS average_rating
"""

TOP_MOVIES_SQL = """
    SELECT
        movies.id,
        movies.title,
        ROUND(AVG(reviews.rating), 1) AS average_rating
    FROM movies
    JOIN reviews ON reviews.movie_id = movies.id
    GROUP BY movies.id
    ORDER BY average_rating DESC, movies.title
    LIMIT ?
"""

LATEST_REVIEWS_SQL = """
    SELECT
        reviews.id,
        movies.title AS movie_title,
        users.name AS user_name,
        reviews.rating
    FROM reviews
    JOIN movies ON reviews.movie_id = movies.id
    JOIN users ON reviews.user_id = users.id
    ORDER BY reviews.publication_date DESC, reviews.id DESC
    LIMIT ? OFFSET 0
"""


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "statistics": fetch_one(SUMMARY_SQL),
        "top_movies": fetch_all(TOP_MOVIES_SQL, [3]),
        "latest_reviews": fetch_all(LATEST_REVIEWS_SQL, [5]),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "404.html", status=404)
