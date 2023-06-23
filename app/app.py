from __future__ import annotations

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from app.core.security import settings

from app.api.api import router


app = FastAPI(title="Wallet_check")

app.include_router(router)


@AuthJWT.load_config
def get_config():
    return settings
