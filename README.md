# КиноОтзыв

КиноОтзыв - Python-проект для хранения фильмов, пользователей, оценок и текстовых отзывов.

## Используемые технологии

Python 3, Django 5.2, Django Template Language (DTL), HTML5, CSS3,
JavaScript, Bootstrap 5.3, JSON для хранения данных, Git, pytest, flake8.

## Веб-интерфейс (Django)

Django-проект `filmreviews` и три приложения:

| Приложение | URL | Имя маршрута | Шаблон |
|---|---|---|---|
| `homepage` | `/` | `homepage:index` | `homepage/index.html` |
| `catalog` | `/movies/` | `catalog:list` | `catalog/movie_list.html` |
| `catalog` | `/movies/<int:movie_id>/` | `catalog:detail` | `catalog/movie_detail.html` |
| `reviews` | `/reviews/` | `reviews:list` | `reviews/review_list.html` |
| `reviews` | `/reviews/<int:review_id>/` | `reviews:detail` | `reviews/review_detail.html` |

Страницы формируются Django-шаблонами. Представления только загружают данные
через `load_system()`, подготавливают словарь `context` и вызывают
`render()`. Функция `page()` из ПР5, собиравшая HTML в Python, удалена.

Для несуществующих фильма или отзыва шаблон показывает сообщение
«не найден» через `{% if %}`, а `render()` возвращает статус `404`.
Для неизвестных адресов подключен `handler404` с шаблоном `templates/404.html`
(виден при `DEBUG = False`).

## Django Template Language

- **Базовый шаблон** `templates/base.html`: `<head>`, Bootstrap, собственный
  CSS, навигация, контейнер страницы, подвал, подключение JavaScript.
  Блоки `{% block title %}` и `{% block content %}` переопределяются
  дочерними шаблонами через `{% extends "base.html" %}`.
- **Включаемые шаблоны** (`{% include %}`):
  - `templates/includes/navigation.html` – меню сайта;
  - `catalog/includes/movie_card.html` – карточка фильма;
  - `reviews/includes/review_verdict.html` – вердикт отзыва
    («Рекомендует» / «Не рекомендует»), используется на трех страницах.
- **Контекст**: например, `{"movies": ...}` в `movie_list()` и
  `{% for movie in movies %}` в шаблоне.
- **Циклы и условия**: `{% for %}` с `{% empty %}` для пустых списков,
  `{% if review.recommended %}`, `{% if movie.reviews %}`, `{% if movie %}`.
- **Фильтры**: `length` (количество фильмов и отзывов), `default`
  (название фильма, имя автора), `date:"d.m.Y"` (дата отзыва),
  `truncatechars:40` (краткий текст в таблице), `floatformat:1`
  (средняя оценка). Фильтры только форматируют данные, бизнес-логика
  остается в `models/` и `services.py`.

## URL-маршрутизация

В каждом `urls.py` приложения задан `app_name`, поэтому маршруты имеют вид
`homepage:index`, `catalog:list`, `catalog:detail`, `reviews:list`,
`reviews:detail`. Ссылки в шаблонах строятся тегом `{% url %}`, например
`{% url 'catalog:detail' movie.movie_id %}`, жестко заданных адресов нет.

## Статические файлы

Каталог `homepage/static/homepage/`:

- `css/style.css` – собственное оформление: карточки статистики и фильмов,
  рейтинг, вердикт отзыва, цитата отзыва, логотип, подвал;
- `js/main.js` – выводит текущий год в подвале и подсвечивает пункт меню
  текущего раздела;
- `img/logo.svg` – логотип в навигации.

Подключение: `{% load static %}` и `{% static 'homepage/css/style.css' %}`.
Проверка: `python manage.py findstatic homepage/img/logo.svg`.

## Хранение данных

Данные по-прежнему хранятся в JSON (`data/`), объекты создаются классами из
`models/`. Django ORM, база данных и формы на текущем этапе не используются –
это задачи следующих практических работ.

## Запуск Django-проекта

```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

После запуска откройте:

- `http://127.0.0.1:8000/`;
- `http://127.0.0.1:8000/movies/`;
- `http://127.0.0.1:8000/movies/1/`;
- `http://127.0.0.1:8000/reviews/`;
- `http://127.0.0.1:8000/reviews/1/`;
- `http://127.0.0.1:8000/movies/999/`.

## Что реализовано

- коллекции объектов фильмов, пользователей и отзывов;
- поиск фильмов по названию, жанру и режиссеру;
- фильтрация фильмов по жанру;
- сортировка и вывод лучших фильмов по среднему рейтингу;
- статистика по жанрам и рейтингам;
- добавление фильмов, пользователей и отзывов;
- проверка корректности оценки от 1 до 10;
- загрузка и сохранение данных в JSON;
- автоматические тесты pytest.

## Объектная модель

### `Movie`

Фильм в каталоге.

Атрибуты: `movie_id`, `title`, `year`, `genre`, `director`, `reviews`.

Методы и свойства:

- `average_rating` - средняя оценка фильма;
- `add_review()` - добавляет отзыв к фильму;
- `latest_review()` - возвращает последний отзыв;
- `has_genre()` - проверяет жанр;
- `to_dict()` и `from_dict()` - преобразование для JSON;
- `__str__()` - строковое представление фильма.

### `User`

Пользователь системы.

Атрибуты: `user_id`, `name`, `registration_date`.

Методы: `to_dict()`, `from_dict()`, `__str__()`.

### `Review`

Отзыв пользователя на фильм.

Атрибуты: `review_id`, `movie_id`, `user_id`, `rating`, `text`, `publication_date`, `recommended`.

Методы и свойства:

- `rating` - свойство с проверкой значения от 1 до 10;
- `is_positive()` - проверяет, является ли отзыв положительным;
- `to_dict()` и `from_dict()` - преобразование для JSON;
- `__str__()` - строковое представление отзыва.

### `FilmReviewSystem`

Класс, который организует взаимодействие объектов.

Методы:

- `add_movie()` - добавляет фильм;
- `add_user()` - добавляет пользователя;
- `add_review()` - создает отзыв и связывает его с фильмом и пользователем;
- `get_movie()` и `get_user()` - поиск объектов по идентификатору.

## Структура проекта

```text
Film_review_system/
├── data/
│   ├── movies.json
│   ├── reviews.json
│   └── users.json
├── filmreviews/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   ├── includes/
│   │   └── navigation.html
│   ├── 404.html
│   └── base.html
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── img/logo.svg
│   │   └── js/main.js
│   ├── templates/homepage/index.html
│   ├── urls.py
│   └── views.py
├── catalog/
│   ├── templates/catalog/
│   │   ├── includes/movie_card.html
│   │   ├── movie_detail.html
│   │   └── movie_list.html
│   ├── urls.py
│   └── views.py
├── reviews/
│   ├── templates/reviews/
│   │   ├── includes/review_verdict.html
│   │   ├── review_detail.html
│   │   └── review_list.html
│   ├── urls.py
│   └── views.py
├── tests/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_storage.py
├── main.py
├── manage.py
├── models/
├── services.py
├── storage.py
├── requirements.txt
└── README.md
```

## JSON-данные

Данные хранятся в трех файлах:

- `data/movies.json` - фильмы;
- `data/users.json` - пользователи;
- `data/reviews.json` - отзывы.

В JSON сохраняются обычные словари и списки. При запуске они преобразуются в объекты `Movie`, `User` и `Review`, а при сохранении объекты снова переводятся в JSON-структуры.

## Создание виртуального окружения

```bash
py -m venv venv
```

## Активация окружения

```bash
.\venv\Scripts\Activate.ps1
```

## Установи зависимости

```bash
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Запуск проекта

```bash
.\venv\Scripts\python.exe main.py
```

Если файлы данных пустые или отсутствуют, программа создаст демонстрационные данные.

## Тесты

Запуск тестов:

```bash
.\venv\Scripts\python.exe -m pytest
```

Проверка стиля:

```bash
.\venv\Scripts\python.exe -m flake8 .
```

## Дальнейшее развитие

Перевод хранения данных из JSON в базу данных и Django ORM, формы Django,
создание и редактирование фильмов и отзывов через веб-интерфейс.
