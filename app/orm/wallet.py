from __future__ import annotations

from datetime import datetime as dt
from sqlalchemy import String, DateTime
from app.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from .user_wallet import user_wallet_table

if TYPE_CHECKING:
    from .user import UserModel


class WalletModel(ORMModel):

    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)
    wallets: Mapped[List[UserModel]] = relationship(
        "WalletModel",
        secondary=user_wallet_table,
        back_populates="users"
    )
