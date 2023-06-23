from fastapi import APIRouter
from corecrud import Values, Where
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from starlette import status
from app.core.security import hash_password
from app.core.crud import crud
from app.core.depends import DatabaseSession
from app.orm import UserModel
from app.schemas import (
    ApplicationResponse,
    BodyRegisterRequest,
    RouteReturnT
)


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

        if await crud.users.select.one(
            Where(UserModel.email == request.email),
            session=session,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        await crud.users.insert.one(
            Values({
                UserModel.email: request.email,
                UserModel.password: hash_password(password=request.password),
            }),
            session=session
        )
    return {
        "ok": True,
        "result": True,
    }
