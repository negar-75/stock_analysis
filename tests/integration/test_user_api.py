import pytest
from httpx import AsyncClient


# ── Success ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_user_success(async_client: AsyncClient):
    payload = {
        "user_name": "testuser",
        "email": "test@example.com",
        "phone": "+351912345678",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }

    response = await async_client.post("/api/v1/user/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["user_name"] == payload["user_name"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


# ── Duplicate ──────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client: AsyncClient):
    payload = {
        "user_name": "testuser",
        "email": "test@example.com",
        "phone": "+351912345678",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }

    first = await async_client.post("/api/v1/user/", json=payload)
    assert first.status_code == 201

    second = await async_client.post("/api/v1/user/", json=payload)
    assert second.status_code == 409
    assert "already exists" in second.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_user_duplicate_username(async_client: AsyncClient):
    first_payload = {
        "user_name": "sameusername",
        "email": "first@example.com",
        "phone": "+351912345678",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }
    second_payload = {
        "user_name": "sameusername",
        "email": "second@example.com",  # different email, same username
        "phone": "+351912345679",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }

    first = await async_client.post("/api/v1/user/", json=first_payload)
    assert first.status_code == 201

    second = await async_client.post("/api/v1/user/", json=second_payload)
    assert second.status_code == 409


# ── Validation ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client: AsyncClient):
    payload = {
        "user_name": "testuser",
        "email": "not-an-email",
        "phone": "+351912345678",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }

    response = await async_client.post("/api/v1/user/", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_passwords_do_not_match(async_client: AsyncClient):
    payload = {
        "user_name": "testuser",
        "email": "test@example.com",
        "phone": "+351912345678",
        "password_1": "StrongPassword123!",
        "password_2": "DifferentPassword123!"
    }

    response = await async_client.post("/api/v1/user/", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_weak_password(async_client: AsyncClient):
    payload = {
        "user_name": "testuser",
        "email": "test@example.com",
        "phone": "+351912345678",
        "password_1": "123",
        "password_2": "123"
    }

    response = await async_client.post("/api/v1/user/", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_missing_fields(async_client: AsyncClient):
    response = await async_client.post("/api/v1/user/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_invalid_phone(async_client: AsyncClient):
    payload = {
        "user_name": "testuser",
        "email": "test@example.com",
        "phone": "not-a-phone",
        "password_1": "StrongPassword123!",
        "password_2": "StrongPassword123!"
    }

    response = await async_client.post("/api/v1/user/", json=payload)
    assert response.status_code == 422