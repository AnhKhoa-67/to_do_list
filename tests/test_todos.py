from fastapi.testclient import TestClient
from sqlmodel import Session

def test_register_and_login(client: TestClient):
    # Register
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_todo_crud(client: TestClient):
    # 1. Login
    client.post("/api/v1/auth/register", json={"email": "user@example.com", "password": "password"})
    login_resp = client.post("/api/v1/auth/login", data={"username": "user@example.com", "password": "password"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create
    response = client.post("/api/v1/todos/", json={"title": "Test Title", "tags": ["tag1"]}, headers=headers)
    assert response.status_code == 200
    todo_id = response.json()["id"]

    # 3. Read
    response = client.get(f"/api/v1/todos/{todo_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"
    assert "tag1" in [t["name"] for t in response.json()["tags"]]

    # 4. Soft Delete
    client.delete(f"/api/v1/todos/{todo_id}", headers=headers)
    response = client.get(f"/api/v1/todos/{todo_id}", headers=headers)
    assert response.status_code == 404
