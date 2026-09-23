from __future__ import annotations

from datetime import date


class User:
    """User of the film review system."""

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
