from fastapi import APIRouter, Depends, HTTPException, status

from stock_analysis.services.users.users import UserService
from stock_analysis.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialError,
)
from stock_analysis.core.security import create_access_token
from stock_analysis.schemas.user import (
    UserCreate,
    UserResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdatePassword,
)
from stock_analysis.api.dependencies import get_current_user, get_user_service
from stock_analysis.db.models.user import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        created_user = await service.create_user(data)
        return created_user
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Username or Email already exists")


@router.post("/login", response_model=UserLoginResponse)
async def login(
    data: UserLoginRequest,
    service: UserService = Depends(get_user_service),
):
    try:
        authenticated_user = await service.authenticate_user(data)

        access_token = create_access_token({"sub": str(authenticated_user.id)})

        return {"access_token": access_token}

    except InvalidCredentialError:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch(
    "/me/password",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def update_password(
    data: UserUpdatePassword,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.update_password(current_user.id, data)

    except InvalidCredentialError:
        raise HTTPException(status_code=401, detail="Old password is incorrect")


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    await service.delete_user(current_user.id)
