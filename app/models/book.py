from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")
    genres: Mapped[list["Genre"]] = relationship(
        secondary="book_genre", back_populates="books"
    )

    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["title"] = self.title
        result["description"] = self.description

        if self.author:
            result["author"] = self.author.name

        if self.genres:
            result["genres"] = [genre.name for genre in self.genres]
        return result

    @classmethod
    def from_dict(cls, book_data):
        author_id = book_data.get("author_id")
        genres = book_data.get("genres", [])

        new_book = cls(
            title=book_data["title"],
            description=book_data["description"],
            author_id=author_id,
            genres=genres,
        )

        return new_book
