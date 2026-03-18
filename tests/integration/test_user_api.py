import pytest


def test_create_user_success(sync_client):
    payload = {
        "user_name": "testuser",
        "email": "test@example.com",
        "phone": "+351912345678",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }

    response = sync_client.post("/api/v1/user/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data
