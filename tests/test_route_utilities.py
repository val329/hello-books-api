import pytest
from app.models.book import Book
from app.models.author import Author
from app.routes.route_utilities import validate_model, add_model, get_models_with_filters
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


def test_create_model_book(client):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    result = add_model(Book, test_data)

    # Assert
    assert isinstance(result, tuple)
    assert result[0]["id"] == 1
    assert result[0]["title"] == "New Book"
    assert result[0]["description"] == "The Best!"
    assert result[1] == 201

def test_create_model_book_missing_data(client):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act & Assert
    # Calling `create_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        result_book = add_model(Book, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"

def test_create_model_author(client):
    # Arrange
    test_data = {
        "name": "New Author"
    }

    # Act
    result = add_model(Author, test_data)

    # Assert
    assert isinstance(result, tuple)
    assert result[0]["id"] == 1
    assert result[0]["name"] == "New Author"
    assert result[1] == 201


def test_get_models_with_filters_one_matching_book(two_saved_books):
    # Act
    result = get_models_with_filters(Book, {"title": "ocean"})

    # Assert
    assert result == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "test_desc"
    }]