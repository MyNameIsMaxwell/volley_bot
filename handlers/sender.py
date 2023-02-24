from aiogram import types

from loader import bot, dp
from config_data import config
from get_user_info import google_sheet_parse
from . import first_connection


@dp.message_handler(commands=['sendall'], user_id=config.ADMINS)
async def sender(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(types.InlineKeyboardButton(text='Записаться на пробное!😍', callback_data='trial_lesson_on'))
        text = message.text[9:]
        users = google_sheet_parse.get_newbie_users_info()[0]
        for user in users:
            await bot.send_message(user, text, reply_markup=keyboard_markup)


@dp.message_handler(commands=['sendfor'], user_id=config.ADMINS)
async def sender_individual(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(types.InlineKeyboardButton(text='Записаться на пробное!😍', callback_data='trial_lesson_on'))
        text = message.text.split(maxsplit=2)[2]
        user = message.text.split(maxsplit=2)[1]
        await bot.send_message(user, text, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.endswith('trial_lesson_on'))
async def inline_trial_callback_handler(query: types.CallbackQuery):
    await first_connection.first_connection_handler(query.message)
