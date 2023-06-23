from fastapi import FastAPI
from app.api.api import router


app = FastAPI(
    title="Wallet_Check"
)

app.include_router(router)
