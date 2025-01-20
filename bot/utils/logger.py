import asyncio
import logging
from logging.handlers import RotatingFileHandler

from bot.config import bot, current_directory, Bot, settings



log_filename = str((current_directory + "/logs/logs.log"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
text_format = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s" )

logging.getLogger("apscheduler").setLevel(logging.WARNING)

file_handler = RotatingFileHandler(filename=log_filename, maxBytes=10*1024*1024, backupCount=20, encoding="UTF-8")

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(text_format)




# Создать консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(text_format)

# Добавить обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)