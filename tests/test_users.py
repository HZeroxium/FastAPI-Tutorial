# tests/test_users.py

from app.schemas.auth import TokenResponse


def test_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI CRUD Application"}


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "securepassword",
            "confirm_password": "securepassword",
        },
    )
    assert response.status_code == 201
    token = TokenResponse(**response.json())
    assert token.access_token is not None
    assert token.token_type == "bearer"
