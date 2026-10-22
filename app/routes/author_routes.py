from flask import Blueprint, abort, make_response, request, Response
from app.models.author import Author
from app.models.book import Book
from .route_utilities import validate_model, add_model, get_models_with_filters
from ..db import db

bp = Blueprint("authors", __name__, url_prefix="/authors")


@bp.get("")
def get_all_authors():
    response = []

    authors = get_models_with_filters(Author, request.args)

    for author in authors:
        response.append(author)
    return response


@bp.post("")
def create_author():

    request_body = request.get_json()
    author = add_model(Author, request_body)

    return author


@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]

    return response


@bp.post("/<author_id>/books")
def create_books_by_author(author_id):

    author = validate_model(Author, author_id)
    request_body = request.get_json()
    request_body["author_id"] = author.id
    book = add_model(Book, request_body)

    return book
