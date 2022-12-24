from aiogram import Bot, Dispatcher
from loguru import logger

from config_data import config


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

logger.add(config.LOG_PATH, format="{time} - {level} - {message}", level="DEBUG", rotation="10 MB", compression="zip")