def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_books(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    for response_book, saved_book in zip(response_body, two_saved_books):
        assert response_book["id"] == saved_book.id
        assert response_book["title"] == saved_book.title
        assert response_book["description"] == saved_book.description


def test_get_one_book(client, two_saved_books):

    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"id": 1, "title": "Ocean Book", "description": "test_desc"}


def test_get_one_book_with_no_records(client, two_saved_books):

    response = client.get("/books/5")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Book 5 not found"}


def test_create_book(client):

    response = client.post(
        "/books", json={"title": "Ocean Book", "description": "test_desc"}
    )
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"id": 1, "title": "Ocean Book", "description": "test_desc"}


def test_create_book_no_request_body(client):
    test_data = {}
    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid data: missing key title"}


def test_create_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid data: missing key title"}


def test_create_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid data: missing key description"}


def test_create_book_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value",
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {"id": 1, "title": "New Book", "description": "The Best!"}


def test_update_book(client, two_saved_books):
    # Arrange
    test_data = {"title": "New Book", "description": "The Best!"}
    # Act
    response = client.put("/books/1", json=test_data)

    # Assert
    assert response.status_code == 204


def test_update_book_id_not_found(client, two_saved_books):
    test_data = {"title": "New Book", "description": "The Best!"}
    # Act
    response = client.put("/books/100", json=test_data)
    request_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert request_body == {"message": "Book 100 not found"}


def test_update_book_invalid_id(client, two_saved_books):
    test_data = {"title": "New Book", "description": "The Best!"}
    # Act
    response = client.put("/books/id", json=test_data)
    request_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert request_body == {"message": "Book id invalid"}


def test_delete_book(client, two_saved_books):
    # Act
    response = client.delete("/books/1")

    # Assert
    assert response.status_code == 204


def test_delete_book_id_not_found(client, two_saved_books):
    # Act
    response = client.delete("/books/100")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 100 not found"}


def test_delete_book_invalid_id(client, two_saved_books):
    # Act
    response = client.delete("/books/id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book id invalid"}

