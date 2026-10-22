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

    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["title"] = self.title
        result["description"] = self.description

        if self.author: 
            result["author"] = self.author.name
        return result

    @classmethod
    def from_dict(cls, book_data):
        new_book = Book(
            title=book_data["title"],
            description=book_data["description"],
            author_id=book_data.get("author_id"),
        )

        return new_book


