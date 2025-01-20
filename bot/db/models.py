

from sqlalchemy import BigInteger, DateTime, Float, func, TIMESTAMP
from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer, String





class Base(AsyncAttrs, DeclarativeBase):
    pass


# Модель для таблицы `cryptotokens`
class CryptoToken(Base):
    __tablename__ = 'cryptotokens'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    token_name = mapped_column(String, nullable=False, index=True)
    token_address = mapped_column(String, nullable=False, index=True, unique=True)
    market_cap = mapped_column(Float)
    creator = mapped_column(String)
    
    created_token_time = mapped_column(
        TIMESTAMP(),
        index=True
    )
    
    datetime_reg = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    

    



