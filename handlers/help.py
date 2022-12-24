from aiogram import types

from loader import dp
from config_data.config import DEFAULT_COMMANDS

@dp.message_handler(commands=['help'])
async def help_command(msg: types.Message):
	text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS if command != 'help']
	await msg.reply('\n'.join(text))
