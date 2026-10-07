from django.http import Http404, HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape

from homepage.views import page
from services import find_review_by_id, get_latest_reviews
from storage import load_system


def review_list(request: HttpRequest) -> HttpResponse:
    system = load_system()
    reviews = get_latest_reviews(system.reviews, limit=len(system.reviews))
    rows = "\n".join(
        f"""
<tr>
  <td>
    <a href="{reverse('review_detail', args=[review.review_id])}">
      #{review.review_id}
    </a>
  </td>
  <td>{escape(review.movie.title)}</td>
  <td>{escape(review.user.name)}</td>
  <td>{review.rating}/10</td>
  <td>{review.publication_date.isoformat()}</td>
</tr>
"""
        for review in reviews
    )
    content = f"""
<h1 class="mb-3">Отзывы</h1>
<table class="table table-striped bg-white">
  <thead>
    <tr>
      <th>Номер</th>
      <th>Фильм</th>
      <th>Автор</th>
      <th>Оценка</th>
      <th>Дата</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
"""
    return page("Отзывы", content)


def review_detail(request: HttpRequest, review_id: int) -> HttpResponse:
    system = load_system()
    review = find_review_by_id(system.reviews, review_id)
    if review is None:
        raise Http404("Review not found.")

    verdict = "рекомендует" if review.recommended else "не рекомендует"
    content = f"""
<h1 class="mb-3">Отзыв #{review.review_id}</h1>
<dl class="row">
  <dt class="col-sm-3">Фильм</dt>
  <dd class="col-sm-9">
    <a href="{reverse('movie_detail', args=[review.movie_id])}">
      {escape(review.movie.title)}
    </a>
  </dd>
  <dt class="col-sm-3">Автор</dt>
  <dd class="col-sm-9">{escape(review.user.name)}</dd>
  <dt class="col-sm-3">Оценка</dt>
  <dd class="col-sm-9">{review.rating}/10</dd>
  <dt class="col-sm-3">Дата</dt>
  <dd class="col-sm-9">{review.publication_date.isoformat()}</dd>
  <dt class="col-sm-3">Вердикт</dt>
  <dd class="col-sm-9">Автор {verdict} фильм.</dd>
</dl>
<p class="lead">{escape(review.text)}</p>
<a class="btn btn-outline-secondary" href="{reverse('review_list')}">
  К списку отзывов
</a>
"""
    return page(f"Отзыв #{review.review_id}", content)
