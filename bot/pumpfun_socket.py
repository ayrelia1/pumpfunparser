import asyncio
import random
import logging
import ssl
import traceback
import websockets
import json

from bot.notify_channel import notify_channel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"

# URL вашего WebSocket-сервера
SOCKET_URL = "wss://frontend-api-v2.pump.fun/socket.io/?EIO=4&transport=websocket"

async def handle_message(websocket):
    """Обработка входящих сообщений."""
    

    async for message in websocket:
        logging.info(f"Получено сообщение: {message}")
        try:
            msg = message.strip()
            
            # Если приходит 2 надо ответить 3, для поддержания коннекта
            if msg.isdigit():
                if int(msg) == 2:
                    await websocket.send('3')
                    
            # Если нет, то это монета, пытаемся обработать
            else:
                
                try:
                    await notify_channel(message)
                except Exception as ex:
                    logging.error(f"Error notify channel, msg - {message}, error - {traceback.format_exc()}")
            
                    
                    
        except Exception as e:
            logging.error(f"Ошибка при обработке сообщения: {e}")

async def connect_with_reconnect():
    """Подключение с реконнектом в случае разрыва."""
    headers = {
        "User-Agent": UA,
    }

    # ssl_context = ssl.create_default_context()  # Используем системные сертификаты
    # Если нужно игнорировать ошибки сертификатов:
    ssl_context = ssl._create_unverified_context()

    while True:
        try:
            async with websockets.connect(SOCKET_URL, extra_headers=headers, ssl=ssl_context) as websocket:
                logging.info("Соединение открыто")

                # Отправьте начальное сообщение
                await websocket.send('40')

                # Запустите обработчик сообщений
                await handle_message(websocket)

        except websockets.ConnectionClosed as e:
            logging.error(f"Соединение закрыто: {e.code, e.reason}")
        except Exception as e:
            logging.error(f"Ошибка: {e}")

        logging.info("Попытка переподключения через 2-3 секунды...")
        await asyncio.sleep(2.5)

async def main():
    """Основная асинхронная функция."""
    await connect_with_reconnect()

if __name__ == "__main__":
    asyncio.run(main())
