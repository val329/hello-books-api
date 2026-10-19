import pytest

from app.models.book import Book

# def test_to_dict():
#     book = Book({"title": "Ocean Book", "description": "test_desc"})

#     result = book.from_dict()
#     assert result == {"title": "Ocean Book", "description": "test_desc"}


def test_from_dict_returns_book():
    book_data = {"title": "Ocean Book", "description": "test_desc"}

    book = Book.from_dict(book_data)

    assert book.title == book_data["title"]
    assert book.description == book_data["description"]


def test_from_dict_with_no_title():
    # Arrange
    book_data = {"description": "The Best!"}

    # Act & Assert
    with pytest.raises(KeyError, match="title"):
        book = Book.from_dict(book_data)


def test_from_dict_with_no_description():
    # Arrange
    book_data = {"title": "New Book"}

    # Act & Assert
    with pytest.raises(KeyError, match="description"):
        book = Book.from_dict(book_data)


def test_from_dict_with_extra_keys_returns_book():
    book_data = {"title": "Ocean Book", "description": "test_desc", "extra": "extra"}

    book = Book.from_dict(book_data)

    assert book.title == book_data["title"]
    assert book.description == book_data["description"]


def test_to_dict_no_missing_data():
    # Arrange
    book_data = Book(id=1, title="Ocean Book", description="test_desc")

    # Act
    result = book_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] == "test_desc"


def test_to_dict_missing_id():
    # Arrange
    book_data = Book(title="Ocean Book", description="test_desc")

    # Act
    result = book_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] is None
    assert result["title"] == "Ocean Book"
    assert result["description"] == "test_desc"


def test_to_dict_missing_title():
    # Arrange
    test_data = Book(id=1, description="test_desc")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] is None
    assert result["description"] == "test_desc"


def test_to_dict_missing_description():
    # Arrange
    test_data = Book(id=1, title="Ocean Book")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] is None
