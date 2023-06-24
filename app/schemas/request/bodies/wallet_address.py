from pydantic import BaseModel, Field
from app.utils.metadata import ETHEREUM_ADDRESS_REGEX


class AddressUpload(BaseModel):
    address: str = Field(..., regex=ETHEREUM_ADDRESS_REGEX)
