from aiogram import types

from loader import bot, dp
from handlers import menu


@dp.message_handler(commands=["price_list"])
async def price_list_handler(message: types.Message):
	price = "<i><b>" + "Наш нынешний прейскурант🏐" + "</b></i>"
	photo = types.InputFile(f"img/price_list.png")
	await bot.send_photo(message.chat.id, photo=photo, caption=price, parse_mode="html")
	await menu.menu_cmd(message)
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)