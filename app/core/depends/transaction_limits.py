from fastapi import HTTPException
from starlette import status


async def check_limit_tr(limit: int) -> int:
    if limit > 9999:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction limits > 10000"
        )
    return limit
