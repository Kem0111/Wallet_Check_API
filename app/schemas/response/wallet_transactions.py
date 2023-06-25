from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Transactions(BaseModel):
    transactions: List[Optional[Dict[str, Any]]]
