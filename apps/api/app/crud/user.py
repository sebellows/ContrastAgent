from app.models.user import User
from app.schemas.user import UserCreateInternal, UserDelete, UserUpdate, UserUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDUser = CRUDAdaptor[User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete, None]
crud_users = CRUDUser(User)
