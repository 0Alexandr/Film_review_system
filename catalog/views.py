from django.http import Http404, HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape

from homepage.views import page
from services import find_movie_by_id, sort_movies_by_rating
from storage import load_system


def movie_list(request: HttpRequest) -> HttpResponse:
    system = load_system()
    movies = sort_movies_by_rating(system.movies)
    rows = "\n".join(
        f"""
<tr>
  <td>
    <a href="{reverse('movie_detail', args=[movie.movie_id])}">
      {escape(movie.title)}
    </a>
  </td>
  <td>{movie.year}</td>
  <td>{escape(movie.genre)}</td>
  <td>{escape(movie.director)}</td>
  <td>{movie.average_rating}/10</td>
</tr>
"""
        for movie in movies
    )
    content = f"""
<h1 class="mb-3">Каталог фильмов</h1>
<table class="table table-striped bg-white">
  <thead>
    <tr>
      <th>Название</th>
      <th>Год</th>
      <th>Жанр</th>
      <th>Режиссер</th>
      <th>Рейтинг</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
"""
    return page("Фильмы", content)


def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    system = load_system()
    movie = find_movie_by_id(system.movies, movie_id)
    if movie is None:
        raise Http404("Movie not found.")

    review_items = "\n".join(
        (
            "<li>"
            f"<a href='{reverse('review_detail', args=[review.review_id])}'>"
            f"Отзыв #{review.review_id}</a>: {review.rating}/10, "
            f"{escape(review.user.name)}"
            "</li>"
        )
        for review in movie.reviews
    )
    if not review_items:
        review_items = "<li>Отзывов пока нет.</li>"

    content = f"""
<h1 class="mb-3">{escape(movie.title)}</h1>
<dl class="row">
  <dt class="col-sm-3">Год</dt>
  <dd class="col-sm-9">{movie.year}</dd>
  <dt class="col-sm-3">Жанр</dt>
  <dd class="col-sm-9">{escape(movie.genre)}</dd>
  <dt class="col-sm-3">Режиссер</dt>
  <dd class="col-sm-9">{escape(movie.director)}</dd>
  <dt class="col-sm-3">Средняя оценка</dt>
  <dd class="col-sm-9">{movie.average_rating}/10</dd>
</dl>
<h2 class="h4">Отзывы</h2>
<ul>{review_items}</ul>
<a class="btn btn-outline-secondary" href="{reverse('movie_list')}">
  К списку фильмов
</a>
"""
    return page(movie.title, content)
