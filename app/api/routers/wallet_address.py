from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Body
from app.core.depends import DatabaseSession
from app.schemas import ApplicationResponse, BodyAddressUploadRequest, WalletAddress, Transactions
from app.core.depends import authorization
from app.orm import WalletModel, UserModel
from starlette import status
from app.utils.db_query import (get_or_create_wallet,
                                show_wallet_addresses,
                                delet_wallet_address as del_wallet)
from app.wallet_analytics.wallet_manager import wallet_manager

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


@router.delete(
    path="/{wallet_id}/deleteAddress",
    summary="WORKS: Dlete wallet addresses from user_info relationship.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def delet_wallet_address(
    wallet_id: int,
    session: DatabaseSession,
    user: UserModel = Depends(authorization)
):
    await del_wallet(
            session=session,
            wallet_id=wallet_id,
            user_id=user.id
    )
    return {
        "ok": True,
        "result": True,
    }


@router.get(
    path="/{address}/getTrasactions",
    summary="WORKS: Add wallet address to database.",
    response_model=ApplicationResponse[Transactions],
    status_code=status.HTTP_200_OK,
)
async def get_wallet_transactions(
    address: str,
    limit: int,
    token_amount: int,
    user: UserModel = Depends(authorization)
):
    return {
        "ok": True,
        "result": await wallet_manager.get_transactions(
            address,
            limit,
            token_amount
        )
    }
