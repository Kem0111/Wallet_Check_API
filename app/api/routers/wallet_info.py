from fastapi import APIRouter, Depends
from fastapi.param_functions import Body
from app.core.depends import authorization
from app.orm.user import UserModel

from app.schemas import ApplicationResponse, BodyWalletTransactionRequest, Transactions
from starlette import status
from app.wallet_analytics.wallet_manager import wallet_manager

router = APIRouter()


@router.get(
    path="/getTrasactions",
    summary="WORKS: Add wallet address to database.",
    response_model=ApplicationResponse[Transactions],
    status_code=status.HTTP_200_OK,
)
async def get_wallet_transactions(
    # request: BodyWalletTransactionRequest,
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
