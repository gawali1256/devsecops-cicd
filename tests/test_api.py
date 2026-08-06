import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version_endpoint(client: TestClient) -> None:
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_create_product(client: TestClient) -> None:
    payload = {"name": "Keyboard", "price": 99.99, "stock": 10, "category": "electronics"}
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]


def test_list_products(client: TestClient) -> None:
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product(client: TestClient) -> None:
    create_response = client.post(
        "/products",
        json={"name": "Mouse", "price": 29.99, "stock": 5, "category": "electronics"},
    )
    product_id = create_response.json()["id"]
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_update_product(client: TestClient) -> None:
    created = client.post(
        "/products",
        json={"name": "Monitor", "price": 150.0, "stock": 2, "category": "electronics"},
    )
    product_id = created.json()["id"]
    response = client.put(
        f"/products/{product_id}",
        json={"name": "Monitor Pro", "price": 180.0, "stock": 3, "category": "electronics"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Monitor Pro"


def test_delete_product(client: TestClient) -> None:
    created = client.post(
        "/products",
        json={"name": "Headphones", "price": 79.0, "stock": 4, "category": "accessories"},
    )
    product_id = created.json()["id"]
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Product deleted"


def test_create_user(client: TestClient) -> None:
    payload = {"username": "alice", "email": "alice@example.com", "password": "secret123"}
    response = client.post("/users", json=payload)
    assert response.status_code == 200
    assert response.json()["username"] == payload["username"]


def test_list_users(client: TestClient) -> None:
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(client: TestClient) -> None:
    created = client.post(
        "/users",
        json={"username": "bob", "email": "bob@example.com", "password": "secret123"},
    )
    user_id = created.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user(client: TestClient) -> None:
    created = client.post(
        "/users",
        json={"username": "carol", "email": "carol@example.com", "password": "secret123"},
    )
    user_id = created.json()["id"]
    response = client.put(
        f"/users/{user_id}",
        json={"username": "carol2", "email": "carol2@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "carol2"


def test_delete_user(client: TestClient) -> None:
    created = client.post(
        "/users",
        json={"username": "dave", "email": "dave@example.com", "password": "secret123"},
    )
    user_id = created.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"


def test_login_endpoint_returns_token(client: TestClient) -> None:
    client.post(
        "/users",
        json={"username": "erin", "email": "erin@example.com", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": "erin", "password": "secret123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_search_products_endpoint(client: TestClient) -> None:
    client.post(
        "/products",
        json={"name": "Laptop", "price": 999.0, "stock": 7, "category": "electronics"},
    )
    response = client.get("/products/search?query=laptop")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_invalid_product_payload(client: TestClient) -> None:
    response = client.post(
        "/products",
        json={"name": "", "price": -1, "stock": -1, "category": ""},
    )
    assert response.status_code == 422


def test_invalid_auth_payload(client: TestClient) -> None:
    response = client.post("/auth/login", json={"username": "", "password": ""})
    assert response.status_code == 422
