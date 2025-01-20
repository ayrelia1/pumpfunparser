import asyncio
from datetime import datetime, timezone
import time

from bot.sql_function import databasework
from bot.config import bot, settings
from bot.pumpfun_api import get_featured_token

import json
import logging
import traceback


semaphore = asyncio.Semaphore(5)



async def start_from_api():
    
    list_tokens = await get_featured_token()

    
    # Создаем задачи для каждой монеты
    tasks = [notify_channel(token) for token in list_tokens]

    # Запускаем все задачи одновременно с учетом ограничения семафора
    await asyncio.gather(*tasks)
    



async def notify_channel(data: dict): # message: str
    
    async with semaphore:
        
        # Убираем префикс "42" и распарсиваем JSON
        # _, json_data = message.split('42', 1)
        # data: dict = json.loads(json_data)[1]

        # Извлекаем нужные данные
        result = {
            "image_url": data.get("image_uri"),
            "symbol": data.get("symbol"),
            "market_cap": data.get("usd_market_cap"),
            "creator": data.get("creator"),
            "created_time": data.get("created_timestamp"),
            "total_supply": data.get("total_supply"),
            "reply_count": data.get("reply_count"),
            "name": data.get("name"),
            "description": data.get("description"),
            "mint": data.get("mint"),
            "url": f"https://pump.fun/coin/{data.get('mint')}"
        }
        
        get_token_in_db = await databasework.get_token_by_token_address(result['mint'])
        if get_token_in_db:
            return
        
        # Проверка условия
        
        
        # Проверка времени создания монеты
        current_time = datetime.now().timestamp()  # Текущее время в UTC (в секундах)
        created_time = result.get("created_time") / 1000  # Переводим `created_timestamp` в секунды
        time_diff = current_time - created_time

        # Вычисляем разницу во времени в минутах
        minutes_ago = int(time_diff // 60)
        
        if time_diff > settings.MAX_CREATED_TIME:
            return
        
        # Проверка маркет капы
        if result['market_cap'] > settings.MAX_MARKET_CAP:
            return
        
        # Уведомляем
        
        
        created_token_time = datetime.fromtimestamp(result.get("created_time") / 1000)
        try:
            await databasework.save_token(
                token_name=result['name'],
                token_address=result['mint'],
                market_cap=result['market_cap'],
                creator=result['creator'],
                created_token_time=created_token_time
            )
            
            await bot.send_message(
                text=(
                    f"<b>💰 Name:</b> {result['name']}\n"
                    f"<b>🪙 CA:</b> \n<code>{result['mint']}</code>\n"
                    f"<b>💵 USD Market Cap:</b> ${int(result['market_cap'])}\n"
                    f'🏞 <a href="{result['image_url']}">Image</a>\n'
                    f"<b>🔗 URL:</b> {result['url']}\n"
                    f"<b>Time ago:</b> {minutes_ago}m ago\n"
                    f"<b>Replies:</b> {result['reply_count']}\n"
                ),
                chat_id=settings.CHANNEL_ID
            )
        except Exception as ex:
            logging.error(ex)

        
        