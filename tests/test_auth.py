"""
Tests d'integration des endpoints d'authentification.
"""

from fastapi import status


class TestAuthRouter:
    def test_register_success(self, client):
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_username(self, client):
        client.post(
            "/auth/register",
            json={
                "username": "duplicate",
                "email": "first@example.com",
                "password": "securepass123",
            },
        )

        response = client.post(
            "/auth/register",
            json={
                "username": "duplicate",
                "email": "second@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_register_duplicate_email(self, client):
        client.post(
            "/auth/register",
            json={
                "username": "firstuser",
                "email": "duplicate@example.com",
                "password": "securepass123",
            },
        )

        response = client.post(
            "/auth/register",
            json={
                "username": "seconduser",
                "email": "duplicate@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_login_success(self, client):
        client.post(
            "/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "securepass123",
            },
        )

        response = client.post(
            "/auth/login",
            json={"email": "login@example.com", "password": "securepass123"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        response = client.post(
            "/auth/login",
            json={"email": "missing@example.com", "password": "wrongpass"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_with_valid_token(self, plain_client):
        reg = plain_client.post(
            "/auth/register",
            json={
                "username": "meuser",
                "email": "me@example.com",
                "password": "securepass123",
            },
        )
        token = reg.json()["access_token"]

        response = plain_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "meuser"
        assert data["email"] == "me@example.com"

    def test_me_without_token(self, plain_client):
        response = plain_client.get("/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
