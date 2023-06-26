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

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)

    users: Mapped[List[UserModel]] = relationship(
        "UserModel",
        secondary=user_wallet_table,
        back_populates="wallets"
    )
