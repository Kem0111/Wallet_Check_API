
from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm import UserModel

from .authorization import authorization, authorization_refresh
from app.orm.config import get_async_session


AuthJWT = Annotated[AuthJWT, Depends()]
Authorization = Annotated[UserModel, Depends(authorization)]
AuthorizationRefresh = Annotated[UserModel, Depends(authorization_refresh)]
DatabaseSession = Annotated[AsyncSession, Depends(get_async_session)]

__all__ = (
    "authorization",
    "AuthJWT",
    "Authorization",
    "AuthorizationRefresh",
    "DatabaseSession",
)
