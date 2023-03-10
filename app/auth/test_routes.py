from fastapi.testclient import TestClient

from ..testing_utils import world


def test_get_all_users(client: TestClient):
    response = client.get("/auth/")
    assert response.json() == [
        {"email": "test@email.com", "id": 1, "username": "some person"}
    ]


def test_post_user(client: TestClient):
    response = client.post(
        "/auth/",
        json={
            "email": "another@email.com",
            "username": "idk something dumb",
            "password": "a password",
        },
    )
    assert response.json() == {
        "id": 2,
        "email": "another@email.com",
        "username": "idk something dumb",
    }


def test_login_valid(client: TestClient):
    user = world.user_factory(id=1)
    response = client.post("/auth/login/", json=user)
    data = response.json()
    data.pop("access_token")
    assert data == {
        "user": {"id": 1, "email": "test@email.com", "username": "some person"},
        "token_type": "bearer",
    }


def test_login_invalid_email(client: TestClient):
    response = client.post(
        "/auth/login/", json=world.user_factory(email="wrong@email.com", id=1)
    )
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_invalid_password(client: TestClient):
    response = client.post(
        "/auth/login/",
        json=world.user_factory(password="wrong password", id=1),
    )
    assert response.json() == {"detail": "Incorrect username or password"}
