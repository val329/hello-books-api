from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from .route_utilities import validate_model
from ..db import db


# 1. Define the blueprint
bp = Blueprint("books", __name__, url_prefix="/books")

@bp.post("")
def create_book():

    request_body = request.get_json()

    try: 
        # title = request_body["title"]
        # description = request_body["description"]
        new_book = Book.from_dict(request_body)
    except KeyError as e:
        response = {"message": f"Invalid data: missing key {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201


@bp.get("")
def get_all_books():
    
    response = []

    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    query = query.order_by(Book.id)
    books = db.session.scalars(query)

    for book in books:
        response.append(book.to_dict())
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
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<book_id>")
def delete_book(book_id):

    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")





'''
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


'''