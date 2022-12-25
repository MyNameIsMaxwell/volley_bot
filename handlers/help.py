from aiogram import types

from loader import dp
from config_data.config import DEFAULT_COMMANDS

@dp.message_handler(commands=['help'])
async def help_command(msg: types.Message):
	text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS if command != 'help']
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(types.InlineKeyboardButton("Что-то не работает?", callback_data="my_contact"))
	keyboard_markup.add(types.InlineKeyboardButton("Дайте мне знать, пожалуйста🙂", url="https://t.me/Lymaxe"))
	await msg.reply('\n'.join(text), reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('my_contact'))
async def inline_schedule_answer_callback_handler(query: types.CallbackQuery):
	await query.answer('Ссылка под этой кнопкой)')