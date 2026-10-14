from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import (
    get_latest_reviews,
    get_rating_statistics,
    get_top_movies,
)
from storage import load_system


def index(request: HttpRequest) -> HttpResponse:
    system = load_system()
    context = {
        "statistics": get_rating_statistics(system.movies),
        "top_movies": get_top_movies(system.movies),
        "latest_reviews": get_latest_reviews(system.reviews),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "404.html", status=404)
