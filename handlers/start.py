from aiogram import types
from loguru import logger

from loader import dp
from . import menu
from database import datawork


@dp.message_handler(commands=['start'])
@logger.catch()
async def send_welcome(msg: types.Message):
    await msg.reply(f'Привет, {msg.from_user.first_name}👋 Я BrestVolleybot. От меня ты можешь узнать расписание тренировок на неделю, либо посмотреть материалы, которые помогут тебе лучше принимать, бить и пасовать)')
    await datawork.add_user(msg)
    await menu.menu_cmd(msg)


