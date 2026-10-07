from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape

from services import (
    get_latest_reviews,
    get_rating_statistics,
    get_top_movies,
)
from storage import load_system


def page(title: str, content: str, status: int = 200) -> HttpResponse:
    """Render a small Bootstrap page without a separate template file."""
    html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} - КиноОтзыв</title>
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet">
</head>
<body class="bg-light">
  <nav class="navbar navbar-expand-lg bg-dark navbar-dark">
    <div class="container">
      <a class="navbar-brand" href="{reverse("home")}">КиноОтзыв</a>
      <div class="navbar-nav">
        <a class="nav-link" href="{reverse("movie_list")}">Фильмы</a>
        <a class="nav-link" href="{reverse("review_list")}">Отзывы</a>
      </div>
    </div>
  </nav>
  <main class="container py-4">
    {content}
  </main>
</body>
</html>"""
    return HttpResponse(html, status=status)


def index(request: HttpRequest) -> HttpResponse:
    system = load_system()
    statistics = get_rating_statistics(system.movies)
    top_movies = get_top_movies(system.movies)
    latest_reviews = get_latest_reviews(system.reviews)

    movie_items = "\n".join(
        (
            "<li>"
            f"<a href='{reverse('movie_detail', args=[movie.movie_id])}'>"
            f"{escape(movie.title)}</a> - {movie.average_rating}/10"
            "</li>"
        )
        for movie in top_movies
    )
    review_items = "\n".join(
        (
            "<li>"
            f"<a href='{reverse('review_detail', args=[review.review_id])}'>"
            f"Отзыв #{review.review_id}</a> на фильм "
            f"{escape(review.movie.title)}"
            "</li>"
        )
        for review in latest_reviews
    )
    content = f"""
<h1 class="mb-3">КиноОтзыв</h1>
<p class="lead">
  Django-страницы для каталога фильмов и пользовательских отзывов.
</p>
<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="p-3 bg-white border rounded">
      <div class="text-muted">Фильмов</div>
      <div class="fs-2">{statistics["movies"]}</div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-3 bg-white border rounded">
      <div class="text-muted">С отзывами</div>
      <div class="fs-2">{statistics["rated_movies"]}</div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-3 bg-white border rounded">
      <div class="text-muted">Средняя оценка</div>
      <div class="fs-2">{statistics["average_rating"]}/10</div>
    </div>
  </div>
</div>
<div class="row g-4">
  <section class="col-md-6">
    <h2 class="h4">Лучшие фильмы</h2>
    <ul>{movie_items}</ul>
  </section>
  <section class="col-md-6">
    <h2 class="h4">Последние отзывы</h2>
    <ul>{review_items}</ul>
  </section>
</div>
"""
    return page("Главная", content)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    content = """
<h1 class="mb-3">Страница не найдена</h1>
<p>Такого адреса нет в системе отзывов о фильмах.</p>
<a class="btn btn-primary" href="/">На главную</a>
"""
    return page("404", content, status=404)
