from typing import Optional

from corecrud import Where
from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud import crud
from app.orm import UserModel

from app.orm.config import get_async_session


async def account(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Optional[UserModel]:
    user = await crud.users.select.one(
        Where(UserModel.id == user_id),
        session=session,
        )
    return user


async def authorization_refresh(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> UserModel:
    authorize.jwt_refresh_token_required()

    return await account(user_id=authorize.get_jwt_subject(), session=session)


async def authorization(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> UserModel:
    authorize.jwt_required()

    return await account(user_id=authorize.get_jwt_subject(), session=session)


async def authorization_optional(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Optional[UserModel]:
    authorize.jwt_optional()

    return await account(user_id=authorize.get_jwt_subject(), session=session)
