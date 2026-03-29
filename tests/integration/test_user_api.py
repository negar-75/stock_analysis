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
    

@pytest.mark.asyncio
async def test_update_password_success(
    async_client: AsyncClient,
    test_user,
    mocker,
):
    # Create a JWT token for the test user
    from stock_analysis.core.security import create_access_token
    
    access_token = create_access_token({"sub": str(test_user.id)})
    
    # Mock the password verification to return True (old password is correct)
    mocker.patch(
        "stock_analysis.services.users.users_service.verify_password",
        return_value=True,
    )

    # Mock the password hashing function
    mocker.patch(
        "stock_analysis.services.users.users_service.get_password_hash",
        return_value="new_hashed_password",
    )

    # Make the PATCH request with JWT token in Authorization header
    response = await async_client.patch(
        "/api/v1/user/me/password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "old_password": "123456789012",
            "new_password": "NewPassword123!",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["user_name"] == test_user.user_name
    assert "id" in data


@pytest.mark.asyncio
async def test_update_password_wrong_old_password(
    async_client: AsyncClient,
    test_user,
    mocker,
):
    from stock_analysis.core.security import create_access_token
    
    access_token = create_access_token({"sub": str(test_user.id)})
    
    # Mock verify_password to return False (old password is incorrect)
    mocker.patch(
        "stock_analysis.services.users.users_service.verify_password",
        return_value=False,
    )

    response = await async_client.patch(
        "/api/v1/user/me/password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "old_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Old password is incorrect"


@pytest.mark.asyncio
async def test_update_password_weak_new_password(
    async_client: AsyncClient,
    test_user,
    mocker,
):
    from stock_analysis.core.security import create_access_token
    
    access_token = create_access_token({"sub": str(test_user.id)})
    
    response = await async_client.patch(
        "/api/v1/user/me/password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "old_password": "123456789012",
            "new_password": "weak",  # Too short, fails validation
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_password_no_auth_token(
    async_client: AsyncClient,
):
    # Test without Authorization header (no token)
    response = await async_client.patch(
        "/api/v1/user/me/password",
        json={
            "old_password": "123456789012",
            "new_password": "NewPassword123!",
        },
    )

    assert response.status_code == 401


# ==================== DELETE USER TESTS ====================

@pytest.mark.asyncio
async def test_delete_user_success(
    async_client: AsyncClient,
    test_user,
):
    """Test successful user deletion with valid JWT token"""
    from stock_analysis.core.security import create_access_token
    
    access_token = create_access_token({"sub": str(test_user.id)})
    
    response = await async_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.asyncio
async def test_delete_user_no_auth_token(
    async_client: AsyncClient,
):
    """Test delete user without JWT token returns 401"""
    response = await async_client.delete(
        "/api/v1/user/me",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_invalid_token(
    async_client: AsyncClient,
):
    """Test delete user with invalid JWT token returns 401"""
    invalid_token = "invalid.jwt.token"
    
    response = await async_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_malformed_header(
    async_client: AsyncClient,
):
    """Test delete user with malformed Authorization header"""
    response = await async_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": "NotBearerFormat"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_twice(
    async_client: AsyncClient,
    test_user,
):
    """Test that deleting an already deleted user returns appropriate error"""
    from stock_analysis.core.security import create_access_token
    
    access_token = create_access_token({"sub": str(test_user.id)})
    
    # First deletion - should succeed
    response1 = await async_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response1.status_code == 204
    
    # Second deletion with same token - user no longer exists
    response2 = await async_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response2.status_code in (401, 404)


@pytest.mark.asyncio
async def test_get_user_after_deletion(
    async_client: AsyncClient,
    test_user,
):
    """Test that getting user profile after deletion returns 401"""
    from stock_analysis.core.security import create_access_token
    
    access_token = create_access_token({"sub": str(test_user.id)})
    
    # Delete the user
    response_delete = await async_client.delete(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_delete.status_code == 204
    
    # Try to get user profile - should fail
    response_get = await async_client.get(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_get.status_code in (401, 404) 

