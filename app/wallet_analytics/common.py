import aiohttp
import json
from typing import Optional
from app.core.settings import etherscan_settings
from fastapi import HTTPException
from starlette import status


class Wallet:
    """
    WalletManager is a base class for managing
    Ethereum wallet-related operations.
    It handles requests to the Etherscan API for fetching transaction data.
    """

    _ETHERSCAN_API_KEY = etherscan_settings.ETHERSCAN_API_KEY
    _DECIMAL_BASE = 10

    def __init__(self, address: str) -> None:
        """
        Initialize the WalletManager with an Ethereum wallet address.
        """
        self.address = address

    async def get_url(self, page: int = 1, offset: int = 10000):
        """
        Returns the URL for fetching token transactions or
        balance of the wallet address.
        """
        return (
            f"https://api.etherscan.io/api?module=account&"
            f"action=tokentx&address={self.address}&startblock=0&"
            f"endblock=99999999&sort=desc&apikey={self._ETHERSCAN_API_KEY}"
            f"&page={page}&offset={offset}"
        )

    async def request(self) -> Optional[dict]:
        """
        Sends a request to the Etherscan API and returns the JSON data.
        In case of errors, returns an error message or None.
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = await self.get_url()

                async with session.get(url) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=502,
                            detail=f"Etherscan API returned non-200 status code: {response.status}",
                        )

                    data = await response.text()
        except aiohttp.ClientError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to make request to Etherscan API"
            )

        data = json.loads(data)

        return data
