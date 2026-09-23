from __future__ import annotations

from datetime import date

from models.movie import Movie
from models.user import User


class Review:
    """User review that connects a movie and a user."""

    MIN_RATING = 1
    MAX_RATING = 10

    def __init__(
        self,
        review_id: int,
        movie: Movie,
        user: User,
        rating: int,
        text: str,
        publication_date: date | None = None,
        recommended: bool = True,
    ) -> None:
        self.review_id = review_id
        self.movie = movie
        self.user = user
        self.rating = rating
        self.text = text
        self.publication_date = publication_date or date.today()
        self.recommended = recommended

    @property
    def movie_id(self) -> int:
        return self.movie.movie_id

    @property
    def user_id(self) -> int:
        return self.user.user_id

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int) -> None:
        if not self.MIN_RATING <= value <= self.MAX_RATING:
            raise ValueError("Rating must be from 1 to 10.")
        self._rating = value

    def is_positive(self) -> bool:
        return self.rating >= 7 and self.recommended

    def __str__(self) -> str:
        verdict = "recommended" if self.recommended else "not recommended"
        return f"Review #{self.review_id}: {self.rating}/10, {verdict}"

    def to_dict(self) -> dict:
        return {
            "review_id": self.review_id,
            "movie_id": self.movie.movie_id,
            "user_id": self.user.user_id,
            "rating": self.rating,
            "text": self.text,
            "publication_date": self.publication_date.isoformat(),
            "recommended": self.recommended,
        }

    @classmethod
    def from_dict(cls, data: dict, movie: Movie, user: User) -> "Review":
        return cls(
            review_id=int(data["review_id"]),
            movie=movie,
            user=user,
            rating=int(data["rating"]),
            text=str(data["text"]),
            publication_date=date.fromisoformat(data["publication_date"]),
            recommended=bool(data["recommended"]),
        )
