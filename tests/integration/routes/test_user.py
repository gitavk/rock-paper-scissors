import app.crud.user

USER_DATA = {"username": "test_user", "password": "secret"}
TEST_JWT = "test_jwt"


def test_create_user(test_client):
    response = test_client.post(
        "/users/",
        json=USER_DATA,
    )
    assert response.status_code == 201
    assert response.json()["username"] == "test_user"


def test_login_exists_user(test_client, monkeypatch):
    monkeypatch.setattr(
        app.crud.user, "create_access_token", lambda data: TEST_JWT or data
    )
    test_client.post(
        "/users/",
        json=USER_DATA,
    )
    response = test_client.post(
        "/login/",
        data=USER_DATA,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert response.json() == {"access_token": TEST_JWT, "token_type": "bearer"}


def test_login_not_exists_user(test_client):
    response = test_client.post(
        "/login/",
        data=USER_DATA,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
