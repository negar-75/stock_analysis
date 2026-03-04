"""
Authentication dependencies for FastAPI endpoints.

Provides JWT-based user authentication via Bearer token.
"""

import os
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from dotenv import load_dotenv

from .service import get_user_service
from stock_analysis.services.users.users import UserService
from stock_analysis.db.models.user import User


load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ.get("ALGORITHM", "HS256")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: UserService = Depends(get_user_service),
) -> User:
    """
    Extract and validate the current user from the Bearer token.

    Decodes the JWT, extracts the user ID, and fetches the user from the database.
    Raises HTTP 401 if the token is invalid or the user is not found.

    Returns:
        The authenticated User model instance.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = service.get_user(UUID(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
