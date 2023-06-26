from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Body
from app.core.depends import DatabaseSession
from app.schemas import (ApplicationResponse,
                         BodyAddressUploadRequest,
                         WalletAddress,
                         Transactions,
                         WalletBalance,
                         RouteReturnT)
from app.core.depends import authorization
from app.orm import WalletModel, UserModel
from starlette import status
from app.utils.db_query import (get_or_create_wallet,
                                show_wallet_addresses,
                                delet_wallet_address as del_wallet)
from app.wallet_analytics.wallet_manager import wallet_manager
from app.core.depends.transaction_limits import check_limit_tr


router = APIRouter()


@router.post(
    path="/addWallet",
    summary="WORKS: Add wallet address to database.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def add_wallet_address(
    session: DatabaseSession,
    request: BodyAddressUploadRequest = Body(...),
    user: UserModel = Depends(authorization)
) -> RouteReturnT:

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
    path="/getWallets",
    summary="WORKS: Get wallet addresses from database.",
    response_model=ApplicationResponse[WalletAddress],
    status_code=status.HTTP_200_OK,
)
async def get_wallet_addresses(
    session: DatabaseSession,
    user: UserModel = Depends(authorization)
) -> RouteReturnT:
    return {
        "ok": True,
        "result": await show_wallet_addresses(
            session=session,
            model=UserModel,
            user_id=user.id
        ),
    }


@router.delete(
    path="/{wallet_id}/deleteWallet",
    summary="WORKS: Dlete wallet addresses from user_info relationship.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def delet_wallet_address(
    wallet_id: int,
    session: DatabaseSession,
    user: UserModel = Depends(authorization)
) -> RouteReturnT:
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
    path="/{address}/getTransactions",
    summary="WORKS: Get wallet transactions.",
    response_model=ApplicationResponse[Transactions],
    status_code=status.HTTP_200_OK,
)
async def get_wallet_transactions(
    address: str,
    token_amount: int,
    limit: int = Depends(check_limit_tr),
    user: UserModel = Depends(authorization)
) -> RouteReturnT:
    return {
        "ok": True,
        "result": await wallet_manager.get_transactions(
            address,
            limit,
            token_amount
        )
    }


@router.get(
    path="/{address}/getBalance",
    summary="WORKS: Get wallet balance.",
    response_model=ApplicationResponse[WalletBalance],
    status_code=status.HTTP_200_OK
)
async def get_wallet_balance(
    address: str,
    user: UserModel = Depends(authorization)
) -> RouteReturnT:
    return {
        "ok": True,
        "result": await wallet_manager.get_balance(
            address,
        )
    }
