
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import List, Tuple, Type
from sqlalchemy import and_


async def get_or_create_wallet(session:  AsyncSession,
                               model: Type[DeclarativeMeta],
                               **kwargs) -> Tuple[DeclarativeMeta, bool]:

    stmt: Select = select(model).where(and_(*(getattr(model, k) == v for k, v in kwargs.items())))
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

    query: Select = select(model).options(joinedload(model.wallets)).where(model.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()

    if user:
        return {"addresses": [wallet.address for wallet in user.wallets]}
    else:
        return {"addresses": []}
