from sqlalchemy import Delete, select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import List, Tuple, Type
from sqlalchemy import and_
from app.orm.user_wallet import user_wallet_table


async def get_or_create_wallet(session:  AsyncSession,
                               model: Type[DeclarativeMeta],
                               **kwargs) -> Tuple[DeclarativeMeta, bool]:

    stmt: Select = select(model).where(
        and_(*(getattr(model, k) == v for k, v in kwargs.items()))
    )
    stmt = stmt.options(joinedload(model.users))
    result = await session.execute(stmt)
    instance = result.scalars().first()

    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)

        return instance, True


async def show_wallet_addresses(session:  AsyncSession,
                                model: Type[DeclarativeMeta],
                                user_id: int) -> List[DeclarativeMeta]:

    query: Select = (
        select(model).
        options(joinedload(model.wallets)).
        where(model.id == user_id)
    )
    result = await session.execute(query)
    user = result.scalars().first()

    res = {"addresses": []}

    for wallet in user.wallets:
        res["addresses"].append(
            {
                "id": wallet.id,
                "address": wallet.address
            }
        )
    return res


async def delet_wallet_address(session:  AsyncSession,
                               wallet_id,
                               user_id: int):

    stmt: Delete = delete(user_wallet_table).where(
        and_(
            user_wallet_table.c.user_id == user_id,
            user_wallet_table.c.wallet_id == wallet_id
        )
    )
    await session.execute(stmt)
    await session.commit()


async def check_duplicates(session: AsyncSession,
                           model: Type[DeclarativeMeta],
                           field: str,
                           value: str):
    query: Select = select(model).where(
            getattr(model, field) == value
        )
    result = await session.execute(query)

    return result.scalars().first()
