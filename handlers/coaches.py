import asyncio
from aiogram import types,filters
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import bot, dp
from database import datawork
from handlers import menu

coaches_info = datawork.coaches_get()
coaches_callback = CallbackData("Тренер", "page")

async def get_coaches_keyboard(page: int = 0):
	keyboard = InlineKeyboardMarkup(row_width=1)
	has_next_page = len(coaches_info) > page + 1

	if page != 0:
		keyboard.add(
			InlineKeyboardButton(text="< Назад", callback_data=coaches_callback.new(page=page - 1))
		)

	keyboard.add(
			InlineKeyboardButton(
				text=f"• {page + 1} •",
				callback_data="dont_click_me"
			)
		)

	if has_next_page:
		keyboard.add(
			InlineKeyboardButton(
				text="Вперёд >",
				callback_data=coaches_callback.new(page=page + 1)
			)
		)

	return keyboard

@dp.message_handler(commands=["coaches"])
async def coaches_index(message):
	coaches_data = coaches_info[0]
	caption = (f"<b>😎{coaches_data.get('name')}</b>\n"
			   f"\n{coaches_data.get('description')}")
	keyboard = await get_coaches_keyboard()  # Page: 0

	await bot.send_photo(
		chat_id=message.chat.id,
		photo=types.InputFile(f"img/{coaches_data.get('photo')}"),
		caption=caption,
		parse_mode="HTML",
		reply_markup=keyboard
	)

	await asyncio.sleep(4)
	await menu.menu_cmd(message)


@dp.callback_query_handler(coaches_callback.filter())
async def coaches_page_handler(query, callback_data: dict):
	page = int(callback_data.get("page"))
	coaches_data = coaches_info[page]
	caption = (f"⭐{coaches_data.get('name')}\n"
			   f"\n{coaches_data.get('description')}")
	keyboard = await get_coaches_keyboard(page)

	photo = types.InputMedia(type="photo", media=types.InputFile(f"img/{coaches_data.get('photo')}"), caption=caption)

	await query.message.edit_media(photo, keyboard)


