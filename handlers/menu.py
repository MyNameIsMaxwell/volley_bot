from aiogram import types

from loader import dp


async def menu_cmd(message: types.Message):
	keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
	item1 = types.KeyboardButton("Расписание📆")
	item2 = types.KeyboardButton('Тренера🧙')
	item3 = types.KeyboardButton("Помощь⚙")
	keyboard_markup.row(item1)
	keyboard_markup.row(item2, item3)

	await message.answer("Выберите вариант:⤵️", reply_markup=keyboard_markup)
	# more_btns_text = (
	# 	"I don't know",
	# 	"Who am i?",
	# 	"Where am i?",
	# 	"Who is there?",
	# )
	# keyboard_markup.add(*(types.KeyboardButton(text) for text in more_btns_text))