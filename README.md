# КиноОтзыв

КиноОтзыв - Python-проект для хранения фильмов, пользователей, оценок и текстовых отзывов.

## Используемые технологии

Python 3, Django 5.2, Django Template Language (DTL), HTML5, CSS3,
JavaScript, Bootstrap 5.3, SQLite и модуль `sqlite3`, SQL, JSON (исходные
данные), Git, pytest, flake8.

## Веб-интерфейс (Django)

Django-проект `filmreviews` и три приложения:

| Приложение | URL | Имя маршрута | Шаблон |
|---|---|---|---|
| `homepage` | `/` | `homepage:index` | `homepage/index.html` |
| `catalog` | `/movies/` | `catalog:list` | `catalog/movie_list.html` |
| `catalog` | `/movies/search/` | `catalog:search` | `catalog/movie_search.html` |
| `catalog` | `/movies/<int:movie_id>/` | `catalog:detail` | `catalog/movie_detail.html` |
| `reviews` | `/reviews/` | `reviews:list` | `reviews/review_list.html` |
| `reviews` | `/reviews/statistics/` | `reviews:statistics` | `reviews/statistics.html` |
| `reviews` | `/reviews/<int:review_id>/` | `reviews:detail` | `reviews/review_detail.html` |

Страницы формируются Django-шаблонами. Представления выполняют SQL-запросы
к базе SQLite, передают результат в словарь `context` и вызывают `render()`.

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
  `{% if review.recommended %}`, `{% if movie.reviews_count %}`, `{% if movie %}`.
- **Фильтры**: `length` (количество фильмов и отзывов), `default`
  (режиссёр, имя автора, текст отзыва), `truncatechars:40` (краткий текст
  в таблице), `floatformat:1` (средняя оценка). Дата отзыва форматируется
  в SQL функцией `strftime('%d.%m.%Y', ...)`.

## URL-маршрутизация

В каждом `urls.py` приложения задан `app_name`, поэтому маршруты имеют вид
`homepage:index`, `catalog:list`, `catalog:search`, `catalog:detail`,
`reviews:list`, `reviews:statistics`, `reviews:detail`. Ссылки в шаблонах строятся тегом `{% url %}`, например
`{% url 'catalog:detail' movie.id %}`, жестко заданных адресов нет.

## Статические файлы

Каталог `homepage/static/homepage/`:

- `css/style.css` – собственное оформление: карточки статистики и фильмов,
  рейтинг, вердикт отзыва, цитата отзыва, логотип, подвал;
- `js/main.js` – выводит текущий год в подвале и подсвечивает пункт меню
  текущего раздела;
- `img/logo.svg` – логотип в навигации.

Подключение: `{% load static %}` и `{% static 'homepage/css/style.css' %}`.
Проверка: `python manage.py findstatic homepage/img/logo.svg`.

## База данных SQLite (ПР7)

На ПР7 данные проекта перенесены из JSON в базу SQLite `data/filmreviews.sqlite`.
Работа с базой выполняется напрямую через SQL и модуль `sqlite3`,
Django ORM пока не используется.

### Структура базы

| Таблица | Поле | Тип | Ограничения |
|---|---|---|---|
| `movies` | `id` | INTEGER | PRIMARY KEY |
| | `title` | TEXT | NOT NULL |
| | `year` | INTEGER | NOT NULL |
| | `genre` | TEXT | NOT NULL |
| | `director` | TEXT | может быть NULL |
| `users` | `id` | INTEGER | PRIMARY KEY |
| | `name` | TEXT | NOT NULL |
| | `registration_date` | TEXT | NOT NULL, `YYYY-MM-DD` |
| `reviews` | `id` | INTEGER | PRIMARY KEY |
| | `movie_id` | INTEGER | NOT NULL, FOREIGN KEY → `movies.id` |
| | `user_id` | INTEGER | NOT NULL, FOREIGN KEY → `users.id` |
| | `rating` | INTEGER | NOT NULL, CHECK 1–10 |
| | `text` | TEXT | может быть NULL (оценка без текста) |
| | `publication_date` | TEXT | NOT NULL, `YYYY-MM-DD` |
| | `recommended` | INTEGER | NOT NULL, 0/1, DEFAULT 1 |

Связи: один фильм – много отзывов, один пользователь – много отзывов.

### Файлы слоя базы данных

- `sql/schema.sql` – команды `CREATE TABLE IF NOT EXISTS` с первичными и
  внешними ключами;
- `sql/queries.sql` – 18 проверенных SQL-запросов с комментариями: списки,
  `WHERE` (`=`, `BETWEEN`, `LIKE`, `IS NULL`), `JOIN`, `LEFT JOIN`,
  `COUNT/AVG/MIN/MAX/SUM`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT/OFFSET`;
- `db/database.py` – `get_connection()` (`PRAGMA foreign_keys = ON`,
  `row_factory = sqlite3.Row`), `fetch_all()` и `fetch_one()`;
- `db/import_json.py` – перенос данных из JSON: создаёт схему, очищает таблицы,
  вставляет записи `executemany()` в порядке `movies` → `users` → `reviews`,
  при ошибке выполняет `rollback()`;
- `db/run_queries.py` – выполняет все запросы из `queries.sql` и печатает
  результаты (проверка запросов без отдельного SQLite CLI).

Создание базы и проверка запросов:

```bash
python -m db.import_json
python -m db.run_queries
```

### Страницы, получающие данные из SQLite

| Страница | Что выполняется в SQL |
|---|---|
| `/` | `COUNT`, `AVG`, лучшие фильмы (`JOIN` + `GROUP BY` + `LIMIT ?`), последние отзывы (`JOIN` + `ORDER BY` + `LIMIT ?`) |
| `/movies/` | рейтинг фильмов: `LEFT JOIN` + `COUNT` + `AVG` + `GROUP BY` |
| `/movies/<id>/` | фильм `WHERE movies.id = ?`, отзывы фильма `JOIN users` |
| `/movies/search/` | поиск по жанру, части названия (`LIKE`) и минимальной оценке (`HAVING`) |
| `/reviews/` | отзывы `JOIN movies JOIN users`, фильтр по вердикту `WHERE` |
| `/reviews/<id>/` | один отзыв `WHERE reviews.id = ?` |
| `/reviews/statistics/` | итоги `COUNT/AVG/MIN/MAX/SUM`, `GROUP BY` по жанрам и пользователям, фильмы с порогом отзывов `HAVING COUNT(...) >= ?` |

Все значения от пользователя (id, жанр, строка поиска, пороги) передаются
в запросы параметрами `?`; конкатенация и f-строки для подстановки значений
не используются.

JSON-файлы `data/*.json` сохранены: это исходные данные для импорта и данные
консольной версии `main.py` (классы `models/`, модуль `storage.py`).
Django ORM, модели Django и формы на текущем этапе не используются.

## Запуск Django-проекта

```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m db.import_json
python manage.py check
python manage.py test
python manage.py runserver
```

После запуска откройте:

- `http://127.0.0.1:8000/`;
- `http://127.0.0.1:8000/movies/`;
- `http://127.0.0.1:8000/movies/1/`;
- `http://127.0.0.1:8000/movies/search/`;
- `http://127.0.0.1:8000/reviews/`;
- `http://127.0.0.1:8000/reviews/1/`;
- `http://127.0.0.1:8000/reviews/statistics/`;
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
│   ├── filmreviews.sqlite
│   ├── movies.json
│   ├── reviews.json
│   └── users.json
├── db/
│   ├── __init__.py
│   ├── database.py
│   ├── import_json.py
│   ├── run_queries.py
│   └── testing.py
├── sql/
│   ├── queries.sql
│   └── schema.sql
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
│   │   ├── movie_list.html
│   │   └── movie_search.html
│   ├── urls.py
│   └── views.py
├── reviews/
│   ├── templates/reviews/
│   │   ├── includes/review_verdict.html
│   │   ├── review_detail.html
│   │   ├── review_list.html
│   │   └── statistics.html
│   ├── urls.py
│   └── views.py
├── tests/
│   ├── test_database.py
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
.\venv\Scripts\python.exe -m pytest -v
.\venv\Scripts\python.exe manage.py test
```

`tests/test_database.py` проверяет схему, внешние ключи, ограничение
`CHECK`, полноту импорта из JSON и выполнение всех запросов из
`sql/queries.sql`. Django-тесты (`tests.py` приложений) работают на
временной копии базы, созданной из JSON (`db/testing.py`).

Проверка стиля:

```bash
.\venv\Scripts\python.exe -m flake8 .
```

## Дальнейшее развитие

Подключение базы данных к Django через модели и Django ORM, миграции,
административная панель, формы Django для создания и редактирования
фильмов и отзывов.
