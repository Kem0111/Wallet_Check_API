from app.orm import UserModel, WalletModel

from corecrud import CRUD, Mappings
from dataclasses import dataclass


@dataclass(init=False, eq=False, repr=False, frozen=True)
class _CRUD:
    raws: CRUD[None] = CRUD(
        model=None,
        cursor_cls=Mappings,
    )
    users: CRUD[UserModel] = CRUD(model=UserModel)
    wallets: CRUD[WalletModel] = CRUD(model=WalletModel)


crud = _CRUD()

__all__ = ("crud",)
