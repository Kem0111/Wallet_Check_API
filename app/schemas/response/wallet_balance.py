from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class WalletBalance(BaseModel):
    balance: List[Optional[Dict[str, Any]]]