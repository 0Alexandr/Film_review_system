from __future__ import annotations

from datetime import date


class User:
    """Пользователь системы отзывов о фильмах."""

    def __init__(
        self,
        user_id: int,
        name: str,
        registration_date: date | None = None,
    ) -> None:
        self.user_id = user_id
        self.name = name
        self.registration_date = registration_date or date.today()

    def __str__(self) -> str:
        return f"{self.name} (id: {self.user_id})"

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "registration_date": self.registration_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=int(data["user_id"]),
            name=str(data["name"]),
            registration_date=date.fromisoformat(data["registration_date"]),
        )


class Review:
    """Отзыв пользователя на конкретный фильм."""

    MIN_RATING = 1
    MAX_RATING = 10

    def __init__(
        self,
        review_id: int,
        movie_id: int,
        user_id: int,
        rating: int,
        text: str,
        publication_date: date | None = None,
        recommended: bool = True,
    ) -> None:
        self.review_id = review_id
        self.movie_id = movie_id
        self.user_id = user_id
        self.rating = rating
        self.text = text
        self.publication_date = publication_date or date.today()
        self.recommended = recommended

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int) -> None:
        if not self.MIN_RATING <= value <= self.MAX_RATING:
            raise ValueError("Оценка должна быть от 1 до 10.")
        self._rating = value

    def is_positive(self) -> bool:
        return self.rating >= 7 and self.recommended

    def __str__(self) -> str:
        verdict = "рекомендует" if self.recommended else "не рекомендует"
        return f"Отзыв #{self.review_id}: {self.rating}/10, {verdict}"

    def to_dict(self) -> dict:
        return {
            "review_id": self.review_id,
            "movie_id": self.movie_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "text": self.text,
            "publication_date": self.publication_date.isoformat(),
            "recommended": self.recommended,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Review":
        return cls(
            review_id=int(data["review_id"]),
            movie_id=int(data["movie_id"]),
            user_id=int(data["user_id"]),
            rating=int(data["rating"]),
            text=str(data["text"]),
            publication_date=date.fromisoformat(data["publication_date"]),
            recommended=bool(data["recommended"]),
        )


class Movie:
    """Фильм с коллекцией пользовательских отзывов."""

    def __init__(
        self,
        movie_id: int,
        title: str,
        year: int,
        genre: str,
        director: str,
        reviews: list[Review] | None = None,
    ) -> None:
        self.movie_id = movie_id
        self.title = title
        self.year = year
        self.genre = genre
        self.director = director
        self.reviews = reviews or []

    @property
    def average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        rating_sum = sum(review.rating for review in self.reviews)
        return round(rating_sum / len(self.reviews), 1)

    def add_review(self, review: Review) -> None:
        if review.movie_id != self.movie_id:
            raise ValueError("Отзыв относится к другому фильму.")
        self.reviews.append(review)

    def latest_review(self) -> Review | None:
        if not self.reviews:
            return None
        return max(self.reviews, key=lambda review: review.publication_date)

    def has_genre(self, genre: str) -> bool:
        return self.genre.lower() == genre.lower()

    def __str__(self) -> str:
        return (
            f"{self.title} ({self.year}), {self.genre}, "
            f"рейтинг {self.average_rating}/10"
        )

    def to_dict(self) -> dict:
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
            "director": self.director,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        reviews: list[Review] | None = None,
    ) -> "Movie":
        return cls(
            movie_id=int(data["movie_id"]),
            title=str(data["title"]),
            year=int(data["year"]),
            genre=str(data["genre"]),
            director=str(data["director"]),
            reviews=reviews,
        )


class FilmReviewSystem:
    """Объединяет фильмы, пользователей и отзывы в одну объектную модель."""

    def __init__(
        self,
        movies: list[Movie] | None = None,
        users: list[User] | None = None,
        reviews: list[Review] | None = None,
    ) -> None:
        self.movies = movies or []
        self.users = users or []
        self.reviews = reviews or []
        self._attach_reviews_to_movies()

    def _attach_reviews_to_movies(self) -> None:
        reviews_by_movie: dict[int, list[Review]] = {}
        for review in self.reviews:
            reviews_by_movie.setdefault(review.movie_id, []).append(review)
        for movie in self.movies:
            movie.reviews = reviews_by_movie.get(movie.movie_id, [])

    def add_movie(
        self,
        title: str,
        year: int,
        genre: str,
        director: str,
    ) -> Movie:
        movie = Movie(
            movie_id=self._next_id([movie.movie_id for movie in self.movies]),
            title=title,
            year=year,
            genre=genre,
            director=director,
        )
        self.movies.append(movie)
        return movie

    def add_user(self, name: str) -> User:
        user = User(
            user_id=self._next_id([user.user_id for user in self.users]),
            name=name,
        )
        self.users.append(user)
        return user

    def add_review(
        self,
        movie_id: int,
        user_id: int,
        rating: int,
        text: str,
        recommended: bool = True,
    ) -> Review:
        movie = self.get_movie(movie_id)
        self.get_user(user_id)
        review = Review(
            review_id=self._next_id(
                [review.review_id for review in self.reviews]
            ),
            movie_id=movie_id,
            user_id=user_id,
            rating=rating,
            text=text,
            recommended=recommended,
        )
        self.reviews.append(review)
        movie.add_review(review)
        return review

    def get_movie(self, movie_id: int) -> Movie:
        for movie in self.movies:
            if movie.movie_id == movie_id:
                return movie
        raise ValueError("Фильм не найден.")

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise ValueError("Пользователь не найден.")

    @staticmethod
    def _next_id(values: list[int]) -> int:
        if not values:
            return 1
        return max(values) + 1
