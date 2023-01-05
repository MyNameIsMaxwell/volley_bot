from aiogram import types

from loader import dp


async def menu_cmd(message: types.Message):
	keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
	item1 = types.KeyboardButton('Что дальше💪')
	item2 = types.KeyboardButton("Расписание📆")
	item3 = types.KeyboardButton("Записаться на тренировку🏃🏃‍♀️")
	item4 = types.KeyboardButton("О нас👨‍👩‍👧‍👦")
	item5 = types.KeyboardButton("Помощь⚙")
	keyboard_markup.row(item1, item2)
	keyboard_markup.row(item3)
	keyboard_markup.row(item4, item5)

	await message.answer("Выбери вариант:⤵️", reply_markup=keyboard_markup)
	# more_btns_text = (
	# 	"I don't know",
	# 	"Who am i?",
	# 	"Where am i?",
	# 	"Who is there?",
	# )
	# keyboard_markup.add(*(types.KeyboardButton(text) for text in more_btns_text))