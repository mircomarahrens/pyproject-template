from fastapi.testclient import TestClient

from pyproject_template.api.main import Item, app, get_test, put_item

client = TestClient(app)


def test_get_items_with_query():
    response = client.get("/items/42?q=hello")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "hello"}


def test_get_items_without_query():
    response = client.get("/items/7")
    assert response.status_code == 200
    assert response.json() == {"item_id": 7, "q": None}


def test_put_item_route():
    payload = {"name": "Book", "price": 9.99, "is_offer": True}
    response = client.put("/items/5", json=payload)
    assert response.status_code == 200
    assert response.json() == {"item_name": "Book", "item_id": 5}


def test_numbers_addition_route():
    response = client.get("/numbers/addition/4/17")
    assert response.status_code == 200
    assert response.json() == 21


def test_get_test_generator_values():
    assert list(get_test()) == list(range(10))


def test_put_item_function_directly():
    item = Item(name="Pen", price=1.5, is_offer=None)
    assert put_item(10, item) == {"item_name": "Pen", "item_id": 10}


def test_get_test_endpoint_streaming():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "".join(f"{i}\n" for i in range(10))
