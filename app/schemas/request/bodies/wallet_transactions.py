from pydantic import BaseModel


class WalletTransaction(BaseModel):
    address: str
    limit: int
    token_amount: int
