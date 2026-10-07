# КиноОтзыв

КиноОтзыв - Python-проект для хранения фильмов, пользователей, оценок и текстовых отзывов.

## Практическая работа 5: Django

В проект добавлена Django-часть без удаления кода предыдущей практической
работы. Django использует существующие JSON-файлы и классы проекта.

Что добавлено:

- Django-проект `filmreviews`;
- приложение `homepage` с главной страницей `/` и пользовательской 404;
- приложение `catalog` со страницами `/movies/` и `/movies/<id>/`;
- приложение `reviews` со страницами `/reviews/` и `/reviews/<id>/`;
- тесты страниц в `tests.py` каждого Django-приложения;
- функции `find_movie_by_id()` и `find_review_by_id()` в `services.py`.

Настройки Django:

- язык: `ru-RU`;
- часовой пояс: `Europe/Moscow`;
- `ALLOWED_HOSTS`: `127.0.0.1`, `localhost`, `testserver`;
- подключен обработчик `handler404`.

Запуск Django-проекта:

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

Пользовательская страница 404 на произвольном адресе, например
`/nonexistent/`, видна при `DEBUG = False` в `filmreviews/settings.py`.
После проверки верните значение `True`.

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
├── homepage/
├── catalog/
├── reviews/
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
