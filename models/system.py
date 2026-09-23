from __future__ import annotations

from models.movie import Movie
from models.review import Review
from models.user import User


class FilmReviewSystem:
    """Object model that stores movies, users and reviews together."""

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
        for movie in self.movies:
            movie.reviews = []
        for review in self.reviews:
            review.movie.add_review(review)

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
        movie: Movie,
        user: User,
        rating: int,
        text: str,
        recommended: bool = True,
    ) -> Review:
        self._validate_movie(movie)
        self._validate_user(user)
        review = Review(
            review_id=self._next_id(
                [review.review_id for review in self.reviews]
            ),
            movie=movie,
            user=user,
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
        raise ValueError("Movie not found.")

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise ValueError("User not found.")

    def _validate_movie(self, movie: Movie) -> None:
        if movie not in self.movies:
            raise ValueError("Movie not found.")

    def _validate_user(self, user: User) -> None:
        if user not in self.users:
            raise ValueError("User not found.")

    @staticmethod
    def _next_id(values: list[int]) -> int:
        if not values:
            return 1
        return max(values) + 1
