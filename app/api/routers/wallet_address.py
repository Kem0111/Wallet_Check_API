from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Body
from app.core.depends import DatabaseSession
from app.schemas import ApplicationResponse, BodyAddressUploadRequest
from app.core.depends import authorization
from app.orm import WalletModel, UserModel
from starlette import status
from app.schemas.schema import DictStrAny
from app.utils.db_query import get_or_create_wallet, show_wallet_addresses
from app.schemas.orm.wallet_address import WalletAddress

router = APIRouter()



@router.post(
    path="/addAddress",
    summary="WORKS: Add wallet address to database.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def add_wallet_address(
    session: DatabaseSession,
    request: BodyAddressUploadRequest = Body(...),
    user: UserModel = Depends(authorization)
):

    wallet, created = await get_or_create_wallet(session,
                                                 WalletModel,
                                                 address=request.address)

    if not created and user in wallet.users:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this wallet"
        )

    wallet.users.append(user)
    await session.commit()

    return {
        "ok": True,
        "result": True,
    }


@router.get(
    path="/getAddresses",
    summary="WORKS: Get wallet addresses from database.",
    response_model=ApplicationResponse[WalletAddress],
    status_code=status.HTTP_200_OK,
)
async def get_wallet_addresses(
    session: DatabaseSession,
    user: UserModel = Depends(authorization)
):
    return {
        "ok": True,
        "result": await show_wallet_addresses(
            session=session,
            model=UserModel,
            user_id=user.id
        ),
    }

