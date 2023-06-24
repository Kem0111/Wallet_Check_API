from pydantic import BaseModel
from typing import List, Optional


class WalletAddress(BaseModel):
    addresses: List[Optional[str]]
