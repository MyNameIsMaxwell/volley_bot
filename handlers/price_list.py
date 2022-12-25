from aiogram import types

from loader import bot, dp
from handlers import menu

@dp.message_handler(commands=["price_list"])
async def price_list_handler(message: types.Message):
	price = "<i><b>" + "Наш нынешний прейскурант🏐" + "</b></i>"
	photo = types.InputFile(f"img/price_list.png")
	social_media = "\n<i>" + "Соцсети для связи:" + "</i>"
	text = price + social_media
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(types.InlineKeyboardButton("📷Наш Instagram", url="https://www.instagram.com/brest.volley/"))
	keyboard_markup.add(types.InlineKeyboardButton("🟣Наш Viber-чат", url="https://invite.viber.com/?g=5eswEYG1K0vRF1SWMqOUGuwuqF1OPLKE"))
	await bot.send_photo(message.chat.id, photo=photo, caption=text, parse_mode="html",reply_markup=keyboard_markup)
	await menu.menu_cmd(message)
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)