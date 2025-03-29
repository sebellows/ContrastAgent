from typing_extensions import Annotated

from pydantic import BaseModel, Email, Field, HttpUrl

from app.utils import generate_gravatar_url, DEFAULT_AVATAR_URL

from .mixins import PaginatedResponseSchema, SoftDeletionSchema, TimestampSchema, UUIDSchema


class TokenRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None
    expires_in: int | None = None
    refresh_expires_in: int | None = None

class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    email: Annotated[Email, Field(example="john.warhammer@terra.com")]
    full_name: Annotated[str, Field(min_length=2, max_length=60, example="John Warhammer")]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", example="johnwarhammer")]
    # roles: Optional[list[str]] = []


class UserResponse(UserBase, SoftDeletionSchema, TimestampSchema, UUIDSchema):
    avatar_url: HttpUrl | None = None
    inactive: bool | None = None
    tier_id: int | None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass
    # password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]

    class Config:
        from_attributes = True
        validate_assignment = True


class UserCreateInternal(CreatedTimestampSchema, UserBase):
    pass
    # password_hash: str


class UserUpdate(UserBase):

    class Config:
        from_attributes = True
        validate_assignment = True


class UserTierUpdate(BaseModel):
    tier_id: int

    class Config:
        from_attributes = True
        validate_assignment = True


class UserDelete(BaseModel, SoftDeletionSchema):
    pass


class UserRestoreDeleted(BaseModel):
    is_deleted: bool


class UserPaginatedResponse[PaginatedResponseSchema[UserResponse]]:

    class Config:
        from_attributes = True
