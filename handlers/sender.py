from aiogram import types

from loader import bot, dp
from config_data import config
from database import datawork


@dp.message_handler(commands=['sendall'], user_id=config.ADMINS)
async def sender(message: types.Message):
    if message.from_user.id in config.ADMINS:
        text = message.text[9:]
        users = datawork.get_users_for_message()
        for user in users:
            await bot.send_message(user.user_id, text)

