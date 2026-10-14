from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import find_movie_by_id, sort_movies_by_rating
from storage import load_system


def movie_list(request: HttpRequest) -> HttpResponse:
    system = load_system()
    context = {
        "movies": sort_movies_by_rating(system.movies),
    }
    return render(request, "catalog/movie_list.html", context)


def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    system = load_system()
    movie = find_movie_by_id(system.movies, movie_id)
    context = {
        "movie": movie,
    }
    return render(
        request,
        "catalog/movie_detail.html",
        context,
        status=404 if movie is None else 200,
    )
