import requests
from contextvars import Token

from fastapi import Depends, HTTPException, status

from app.core.auth import get_current_user
from app.core.config import settings
from app.models.user import User

from .api import router


# logger = logging.getLogger(__name__)

# API endpoints
@router.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    """Get token from Keycloak"""
    data = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = response.json()

    return { "access_token": token_data["access_token"], "token_type": "bearer" }


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """A protected route that requires authentication"""
    return {"message": f"Hello, {current_user.username}! This is a protected route."}
