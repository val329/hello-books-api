# class Book: 
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(id=1, title="The Great Gatsby", description="A classic novel about the American Dream."),
#     Book(id=2, title="To Kill a Mockingbird", description="A novel about racial injustice in the Deep South."),
#     Book(id=3, title="1984", description="A dystopian novel about a totalitarian society.")
# ]

from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]