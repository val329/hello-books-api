import pytest
from app.models.book import Book
from app.routes.route_utilities import validate_model
from werkzeug.exceptions import HTTPException


def test_validate_book_valid_id(two_saved_books):
    # Act
    result = validate_model(Book, 1)
    # Assert
    assert result == two_saved_books[0]


def test_validate_book_invalid_id(two_saved_books):
    # #Act
    # result = validate_book(100)
    # #Assert
    # assert result ==  {"message": "book 100 not found"}
    with pytest.raises(HTTPException):
        result = validate_model(Book, "100")


def test_validate_book_id_not_found(two_saved_books):
    with pytest.raises(HTTPException):
        result = validate_model(Book, "id")
