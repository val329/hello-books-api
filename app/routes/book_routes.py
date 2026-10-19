from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db


# 1. Define the blueprint
books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():

    request_body = request.get_json()

    try: 
        title = request_body["title"]
        description = request_body["description"]
        new_book = Book(title=title, description=description)
    except KeyError as e:
        response = {"message": f"Invalid data: missing key {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201


@books_bp.get("")
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
        response.append(
            {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            }
        )
    return response


@books_bp.get("/<book_id>")
def get_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }


@books_bp.put("/<book_id>")
def update_book(book_id):

    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@books_bp.delete("/<book_id>")
def delete_book(book_id):

    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book: 
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))
    
    return book


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