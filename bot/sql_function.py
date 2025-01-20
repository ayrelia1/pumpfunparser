from typing import Dict, List, Optional, Tuple

import pytz
from bot.db.db import async_session, engine
from bot.db.models import CryptoToken

import sys, asyncio
from sqlalchemy import DateTime, and_, cast, desc, func, or_, text, bindparam
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.future import select

import json
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

class databasework:
    
    async def get_token_by_token_address(address: str):
        async with async_session() as session:
            
            stmt = select(CryptoToken).filter_by(token_address=address)
            result = await session.execute(stmt)
            
        return result.scalars().one_or_none()
    
    async def save_token(token_name: str, token_address: str, market_cap: int, creator: str, created_token_time: int):
        async with async_session() as session:
            token = CryptoToken(
                token_name=token_name,
                token_address=token_address,
                market_cap=market_cap,
                creator=creator,
                created_token_time=created_token_time
            )
            session.add(token)
            await session.commit()
        return