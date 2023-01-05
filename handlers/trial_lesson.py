from aiogram import types

from loader import bot, dp


@dp.message_handler(commands=["trial_lesson"])
async def trial_lesson_handler(message: types.Message):
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(types.InlineKeyboardButton("Записаться на тренировку👍",
												   url="https://docs.google.com/forms/d/1WUwwc9Xiv6LQDQFO6TzvbvvbIqOeVPWqklFxNFvLdKw/edit#response=ACYDBNi7m9BjZI-7ySZlWst-bQTnELpAx7AyfUwqjGWh_225xIw_aZVdLbmofDa2XIdodbk"))
	await bot.send_message(message.chat.id, "<em>Если хотите добиться успеха, задайте себе 4 вопроса: Почему? А почему бы и нет? Почему бы и не я? Почему бы и не прямо сейчас?</em>",
							parse_mode="html",
							reply_markup=keyboard_markup
						   )
