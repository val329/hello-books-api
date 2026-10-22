from flask import Blueprint, request, Response
from app.models.book import Book
from .route_utilities import validate_model, add_model, get_models_with_filters
from ..db import db

# 1. Define the blueprint
bp = Blueprint("books", __name__, url_prefix="/books")


@bp.post("")
def create_book():

    request_body = request.get_json()
    book = add_model(Book, request_body)

    return book


@bp.get("")
def get_all_books():

    response = []
    books = get_models_with_filters(Book, request.args)

    for book in books:
        response.append(book)
    return response


@bp.get("/<book_id>")
def get_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):

    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    if request_body.get("author_id"):
        book.description = request_body["author_id"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<book_id>")
def delete_book(book_id):

    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


"""
# When combined with the book_bp's url_prefix, "/books", we see this endpoint is a GET to /books.
# URIs are sensitive to the use of / and Flask will throw an error if we define this route as "/"
# but try to access it as /books. A URI ending in / is different from a URI that doesn't end in /, so we should use "".
@books_bp.get("")
def get_books():
    response = []
    for book in books:
        response.append(
            {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            }
        )
    return response

# by default if we return a dictionary, flask sets 200 response. to override use tuple


"""
