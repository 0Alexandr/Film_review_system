from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.review import Review


class Movie:
    """Film with a collection of user reviews."""

    def __init__(
        self,
        movie_id: int,
        title: str,
        year: int,
        genre: str,
        director: str,
        reviews: list["Review"] | None = None,
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

    def add_review(self, review: "Review") -> None:
        if review.movie is not self:
            raise ValueError("Review belongs to another movie.")
        if review not in self.reviews:
            self.reviews.append(review)

    def latest_review(self) -> "Review | None":
        if not self.reviews:
            return None
        return max(self.reviews, key=lambda review: review.publication_date)

    def has_genre(self, genre: str) -> bool:
        return self.genre.lower() == genre.lower()

    def __str__(self) -> str:
        return (
            f"{self.title} ({self.year}), {self.genre}, "
            f"rating {self.average_rating}/10"
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
        reviews: list["Review"] | None = None,
    ) -> "Movie":
        return cls(
            movie_id=int(data["movie_id"]),
            title=str(data["title"]),
            year=int(data["year"]),
            genre=str(data["genre"]),
            director=str(data["director"]),
            reviews=reviews,
        )
