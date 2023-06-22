from app.orm.config import ORMModel
from sqlalchemy import Integer, Table, Column, ForeignKey


user_wallet_table = Table(
    'user_wallet',
    ORMModel.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('wallet_id', Integer, ForeignKey('wallet.id'), primary_key=True)
)
