from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode



load_dotenv()

    
current_directory = os.path.abspath(os.path.dirname(__file__))
root_path = Path(__file__).parent.parent




class Settings(BaseSettings): # создаем settings class
    CHANNEL_ID: str = os.getenv("BOT_TOKEN")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    
    MAX_MARKET_CAP: int = 8500
    MAX_CREATED_TIME: int = 600

    DATABASE_URL: str =  f"sqlite+aiosqlite:///database.db.sqlite3"

    PROXY_IP: str = os.getenv("BOPROXY_IPT_TOKEN")
    PROXY_PORT: int = os.getenv("PROXY_PORT")
    PROXY_LOGIN: str = os.getenv("PROXY_LOGIN")
    PROXY_PASS: str = os.getenv("PROXY_PASS")
        
settings = Settings()
     
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))





