from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class WalletAddress(BaseModel):
    addresses: List[Optional[Dict[str, Any]]]
