from aiogram import types

from loader import bot, dp
from handlers import hall_location, coaches


@dp.message_handler(commands=["about_us"])
async def about_us_handler(message: types.Message):
	keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
	text_and_data = (
		('Локации залов', 'location'),
		('О школе волейбола', 'about_school'),
		('Программа обучения', 'program'),
		('Этапы подготовки', 'stages'),
		('Как всё проходит', 'trainings'),
		('Что брать с собой', 'training_items'),
		('Об основателе🧙', 'about_team'),
		('Соц.сети📔', 'social_media')
	)
	row_btns = (types.InlineKeyboardButton(text, callback_data=f"about:{data}") for text, data in text_and_data)
	keyboard_markup.add(*row_btns)

	await bot.send_message(message.chat.id, "Узнай о <b>нас</b> и <b>наших</b> занятиях больше☀️🏐☀️", parse_mode='html', reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.endswith('location'))
async def inline_location_callback_handler(query: types.CallbackQuery):
	await hall_location.start_location_handler(query.message)


@dp.callback_query_handler(lambda c: c.data.endswith('about_school'))
async def inline_school_callback_handler(query: types.CallbackQuery):
	await query.message.answer("Coming soon..")


@dp.callback_query_handler(lambda c: c.data.endswith('program'))
async def inline_program_callback_handler(query: types.CallbackQuery):
	await query.message.answer("Coming soon..")


@dp.callback_query_handler(lambda c: c.data.endswith('stages'))
async def inline_stages_callback_handler(query: types.CallbackQuery):
	await query.message.answer("Coming soon..")


@dp.callback_query_handler(lambda c: c.data.endswith('trainings'))
async def inline_trainings_callback_handler(query: types.CallbackQuery):
	await query.message.answer("Coming soon..")


@dp.callback_query_handler(lambda c: c.data.endswith('training_items'))
async def inline_items_callback_handler(query: types.CallbackQuery):
	await query.message.answer("Coming soon..")


@dp.callback_query_handler(lambda c: c.data.endswith('about_team'))
async def inline_coaches_callback_handler(query: types.CallbackQuery):
	await coaches.coaches_index(query.message)


@dp.callback_query_handler(lambda c: c.data.endswith('social_media'))
async def inline_social_callback_handler(query: types.CallbackQuery):
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(types.InlineKeyboardButton("📷Наш Instagram", url="https://www.instagram.com/brest.volley/"))
	keyboard_markup.add(types.InlineKeyboardButton("✈️Наш Telegram-чат", url="https://t.me/BRESTVOLLEYball"))
	keyboard_markup.add(types.InlineKeyboardButton("🟣Наш Viber-чат", url="https://invite.viber.com/?g=5eswEYG1K0vRF1SWMqOUGuwuqF1OPLKE"))
	keyboard_markup.add(types.InlineKeyboardButton("🔵Наш VK", url="https://vk.com/brestvolley"))
	keyboard_markup.add(types.InlineKeyboardButton("🖥Наш Сайт", url="http://brestvolley.by/"))
	social_media = "\n<i>" + "Соцсети для связи:📬" + "</i>"
	await bot.send_message(query.message.chat.id, text=social_media, parse_mode='html', reply_markup=keyboard_markup)
	# await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)

