import requests
from typing import Any

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core import async_get_db, settings
from app.core.exceptions.http_exceptions import UnauthorizedException
from app.crud.user import crud_users
from app.models.user import User


oauth2_scheme = settings.OAUTH2_TOKEN_URL


def get_keycloak_public_key():
    """Get the public key from Keycloak for token verification"""
    url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch Keycloak public key",
        )
    return response.json()["public_key"]


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify the JWT token"""
    try:
        public_key = get_keycloak_public_key()
        decoded_token = jwt.decode(
            token,
            f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----",
            algorithms=["RS256"],
            audience=settings.KEYCLOAK_CLIENT_ID,
        )
        return decoded_token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token(token: str) -> bool:
    try:
        token_data = decode_token(token)
        return True if isinstance(token_data, dict) and 'email' in token_data else False
    except Exception:
        return False


async def get_current_user(token: str = Depends(settings.OAUTH2_TOKEN_URL), db: AsyncSession = Depends(async_get_db)) -> User:
    """Get current user based on the JWT token"""
    token_data = decode_token(token)
    email = token_data.get("email", "")
    user = crud_users.get(db=db, email=email, is_deleted=False)

    if user:
        return user
    raise UnauthorizedException("User not authenticated.")


# async def create_current_user(token: str = Depends(settings.OAUTH2_TOKEN_URL), db: AsyncSession = Depends(get_async_db)) -> User:
#     """Get current user based on the JWT token"""
#     token_data = decode_token(token)
#     email = token_data.get("email", "")
#     user = crud_users.get(db=db, email=email, is_deleted=False)

#     return User(
#         username=token_data.get("preferred_username", ""),
#         email=token_data.get("email", ""),
#         full_name=token_data.get("name", ""),
#     )
