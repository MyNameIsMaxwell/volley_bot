from aiogram import types

from . import schedule
from loader import bot, dp


@dp.message_handler(text="Что дальше💪")
async def first_connection_handler(message: types.Message):
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(types.InlineKeyboardButton("Анкета об уровне подготовки👍",
												   url="https://docs.google.com/forms/d/1WUwwc9Xiv6LQDQFO6TzvbvvbIqOeVPWqklFxNFvLdKw/edit#response=ACYDBNi7m9BjZI-7ySZlWst-bQTnELpAx7AyfUwqjGWh_225xIw_aZVdLbmofDa2XIdodbk"))
	keyboard_markup.add(types.InlineKeyboardButton("Расписание📆", callback_data="schedule"))
	keyboard_markup.add(types.InlineKeyboardButton('Связь с нами📲', callback_data="social_media"))
	text = "<b>Шаг 1:</b> Ознакомиться с расписанием.\n<b>Шаг 2:</b> Заполнить анкету и указать свой уровень подготовки💪\n<b>Шаг 3:</b> Выбрать удобный для себя день в расписании и записаться на пробную тренировку (в Директ, мессенджер или позвонить)👐\n<i><em>Важно:</em> Всего за <b>10</b> рублей, Вы сможете весело и с пользой провести время. Мы так же физически развиваем, как тренажерный зал, только в разы приятнее😊</i>"
	await bot.send_message(message.chat.id, text=text, parse_mode="html", reply_markup=keyboard_markup)
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.callback_query_handler(lambda c: c.data.startswith('schedule'))
async def inline_schedule_callback_handler(query: types.CallbackQuery):
	await schedule.start_schedule_handler(query.message)
