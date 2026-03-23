import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from jose import jwt
import os


    
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

@pytest.fixture
async def test_user(session):
    from stock_analysis.db.models import User
    from stock_analysis.core.security import get_password_hash

    user = User(
        user_name="testuser",
        phone="123456789",
        email="test@example.com",
        hashed_password=get_password_hash("123456789012"),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.mark.asyncio
async def test_login_sucess(async_client: AsyncClient, test_user,mocker):
    mocker.patch("stock_analysis.services.users.users_service.verify_password", return_value=True)
    response = await async_client.post("/api/v1/user/login", json = {"email":"test@example.com", "password":"123456789012"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)


@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient, test_user, mocker):
    mocker.patch(
        "stock_analysis.services.users.users_service.verify_password", 
        return_value=False,
    )

    response = await async_client.post(
        "/api/v1/user/login",
        json={
            "email": test_user.email,
            "password": "123456789013",
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_login_invalid_email(async_client: AsyncClient,test_user):
    response = await async_client.post(
        "/api/v1/user/login", 
        json={
            "email": "notfound@example.com",
            "password": "any_password",
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid email or password"

 
@pytest.mark.asyncio
async def test_login_token_content(async_client:AsyncClient , test_user, mocker):
    mocker.patch( "stock_analysis.services.users.users_service.verify_password", return_value=True)

    response = await async_client.post("/api/v1/user/login", json = {"email":"test@example.com","password":"anything"})
    assert response.status_code == 200

    data = response.json()
    token = data["access_token"]
    decoded = jwt.decode(token,os.getenv("SECRET_KEY"),os.getenv("ALGORITHM","HS256"))

    assert decoded["sub"] == data["id"]
    assert "exp" in decoded


async def test_login_missing_email(async_client: AsyncClient,test_user):
    reponse = await async_client.post("/api/v1/user/login" , json={"email":"test@example.com"})
    assert reponse.status_code == 422
    
    

