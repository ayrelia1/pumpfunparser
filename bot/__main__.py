
import logging
import asyncio

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.db.create_tables import create_tables
from bot.db.db import engine
from bot.config import dp, bot, current_directory, root_path

from bot.utils.logger import logger

#from bot.notify_channel import notify_channel

#from bot.pumpfun_socket import connect_with_reconnect
from bot.notify_channel import start_from_api
        
        
schedulers = AsyncIOScheduler(timezone='Europe/Moscow')
                

async def main() -> None:     # функция запуска бота
    
    await create_tables()
    logging.error(f"BOT STARTED")
    
    schedulers.add_job(start_from_api, 'interval', seconds=1, id='start_from_api', max_instances=3)  # Обновление информации РК
    schedulers.start()
    
    #await connect_with_reconnect()
    await asyncio.Event().wait()

    await engine.dispose()
    schedulers.shutdown()
    
    

        
        
    
if __name__ == "__main__":
                
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:
        logging.error('exit')