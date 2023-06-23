from __future__ import annotations

from datetime import datetime as dt
from sqlalchemy import DateTime, String
from app.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from .user_wallet import user_wallet_table

if TYPE_CHECKING:
    from .wallet import WalletModel


class UserModel(ORMModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)
    wallets: Mapped[List[WalletModel]] = relationship(
        "WalletModel",
        secondary=user_wallet_table,
        back_populates="users"
    )
