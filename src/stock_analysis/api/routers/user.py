from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from stock_analysis.api.schemas.user import (
    UserCreate,
    UserResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdate
)
from sqlalchemy.orm import Session
from stock_analysis.api.dependencies.db import get_db
from stock_analysis.services.users.users import UserService
from stock_analysis.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialError,
)
from stock_analysis.api.security import create_access_token

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = UserService(db).create_user(data)
        return created_user
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Username or Email already exists")


@router.post("/login", response_model=UserLoginResponse)
def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        founded_user = UserService(db).authenticate_user(data)
        access_token = create_access_token({"sub": str(founded_user.id)})
        return {"access_token": access_token}
    except InvalidCredentialError:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    

# @router.patch("/{id}")
# def update_user(data:UserUpdate,db:Session = Depends(get_db)):



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID, db: Session = Depends(get_db)):
    deleted = UserService(db).delete_user(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User has not been found")
    return {"message": "User deleted successfully"}
