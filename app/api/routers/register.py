from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from starlette import status

from app.core.security import hash_password
from app.core.depends import DatabaseSession
from app.orm import UserModel
from app.schemas import (
    ApplicationResponse,
    BodyRegisterRequest,
    RouteReturnT
)
from app.utils.db_query import check_duplicates

router = APIRouter()


@router.post(
    path="/",
    summary="WORKS: User registration.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def register_user(
    session: DatabaseSession,
    request: BodyRegisterRequest = Body(...),
) -> RouteReturnT:

    async with session.begin():

        if await check_duplicates(session,
                                  UserModel,
                                  'username',
                                  request.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already registered",
            )

        if await check_duplicates(session,
                                  UserModel,
                                  'email',
                                  request.email):

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        new_user = UserModel(
            username=request.username,
            email=request.email,
            password=hash_password(password=request.password),
        )
        session.add(new_user)
    return {
        "ok": True,
        "result": True,
    }
