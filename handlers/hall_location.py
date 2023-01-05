from aiogram import types

from loader import bot, dp
from database import datawork
from handlers import menu


@dp.message_handler(commands=["gyms_location"])
async def start_location_handler(message: types.Message):
	locations_info = await datawork.locations_get()
	keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
	row_btns = (types.InlineKeyboardButton(text["name"], callback_data=f'gym_id:{index+1}') for index, text in enumerate(locations_info))
	keyboard_markup.add(*row_btns)

	await message.answer(f"Выберите интересующую локацию🏠:", reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('gym_id:'))
async def inline_location_answer_callback_handler(query: types.CallbackQuery):
	answer_data = query.data[-1:]
	locations_info = await datawork.locations_get(answer_data)
	try:
		for location in locations_info:
			if location["id"] == int(answer_data):
				text = (f"🏨Название: {location['name']}\n"
						f"🛤Улица: {location['street_name']}\n"
						)
				keyboard_markup = types.InlineKeyboardMarkup()
				keyboard_markup.add(types.InlineKeyboardButton('Показать на карте', url=f"{location['map_location']}"))
				await types.ChatActions.upload_photo()
				if location['photo'] != 'None':
					photo = types.InputFile(f"img/{location['photo']}")
					await bot.send_photo(query.message.chat.id, photo=photo, caption=text,reply_markup=keyboard_markup)
				else:
					text = '<b>' + text + '</b>'
					await bot.send_message(query.message.chat.id, text, parse_mode="html", reply_markup=keyboard_markup)
	except Exception as exp:
		print(exp)
		text = f'Unexpected callback data {answer_data!r}!'

	await menu.menu_cmd(query.message)
	await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
