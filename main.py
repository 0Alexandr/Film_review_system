from models import FilmReviewSystem
from services import (
    find_movies,
    get_genre_statistics,
    get_latest_reviews,
    get_rating_statistics,
    get_top_movies,
)
from storage import load_system, save_system


def create_demo_system() -> FilmReviewSystem:
    """Создать демонстрационные данные, если JSON-файлы еще пустые."""
    system = FilmReviewSystem()

    interstellar = system.add_movie(
        title="Интерстеллар",
        year=2014,
        genre="Фантастика",
        director="Кристофер Нолан",
    )
    parasite = system.add_movie(
        title="Паразиты",
        year=2019,
        genre="Драма",
        director="Пон Джун-хо",
    )

    alexey = system.add_user("Алексей")
    marina = system.add_user("Марина")

    system.add_review(
        movie=interstellar,
        user=alexey,
        rating=10,
        text="Сильная научная фантастика с эмоциональным финалом.",
        recommended=True,
    )
    system.add_review(
        movie=parasite,
        user=marina,
        rating=9,
        text="Остроумная и напряженная социальная драма.",
        recommended=True,
    )
    return system


def show_catalog(system: FilmReviewSystem) -> None:
    print("Каталог фильмов:")
    for movie in system.movies:
        print(f"- {movie}")


def show_statistics(system: FilmReviewSystem) -> None:
    rating_statistics = get_rating_statistics(system.movies)
    print("\nСтатистика:")
    print(f"Всего фильмов: {rating_statistics['movies']}")
    print(f"Фильмов с отзывами: {rating_statistics['rated_movies']}")
    print(
        "Средний рейтинг каталога: "
        f"{rating_statistics['average_rating']}/10"
    )
    print(f"Фильмы по жанрам: {get_genre_statistics(system.movies)}")


def main() -> None:
    system = load_system()
    if not system.movies:
        system = create_demo_system()
        save_system(system)

    show_catalog(system)

    print("\nЛучшие фильмы:")
    for movie in get_top_movies(system.movies):
        print(f"- {movie.title}: {movie.average_rating}/10")

    print("\nПоиск по запросу 'драма':")
    for movie in find_movies(system.movies, "драма"):
        print(f"- {movie}")

    print("\nПоследние отзывы:")
    for review in get_latest_reviews(system.reviews):
        user = system.get_user(review.user_id)
        movie = system.get_movie(review.movie_id)
        print(f"- {user.name} о фильме '{movie.title}': {review.text}")

    show_statistics(system)


if __name__ == "__main__":
    main()
