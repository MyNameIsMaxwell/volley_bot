from aiogram import types
from datetime import datetime

from get_user_info import google_sheet_parse
from loader import bot, dp
from database import datawork
from handlers import menu


month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
			  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

week_day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


async def current_date_func():
	current_date_value = datetime.now()
	today_date = current_date_value.strftime(f'%d %m %Y')
	today_date = today_date[:3] + month_list[int(today_date[3:5]) - 1] + today_date[5:]
	return current_date_value, today_date


@dp.message_handler(commands=["schedule"])
async def start_schedule_handler(message: types.Message):
	keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
	text_and_data = (
		('Понедельник', 'Понедельник'),
		('Вторник', 'Вторник'),
		('Среда', 'Среда'),
		('Четверг', 'Четверг'),
		('Пятница', 'Пятница'),
		('Суббота', 'Суббота'),
		('Воскресенье', 'Воскресенье'),
		('Неделя', 'Неделя'),
	)
	row_btns = (types.InlineKeyboardButton(text, callback_data=f"day:{data}") for text, data in text_and_data)
	keyboard_markup.add(*row_btns)

	current_date, today_date = await current_date_func()
	await message.reply(f"Сегодня: {today_date} - {week_day[datetime.weekday(current_date)]} 📅\nТренировки на неделю:",
						reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('day:'))
async def inline_schedule_answer_callback_handler(query: types.CallbackQuery):
	answer_data = query.data[4:]
	await query.answer(f'{answer_data}')
	try:
		result = await datawork.schedule_get(answer_data)
		text = await text_create(result, answer_data)
	except Exception as exp:
		print(exp)
		text = f'В этот день у нас тренировок нет🤗'
	# if new_user is True:
	# 	keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
	# 	keyboard_markup.add(types.InlineKeyboardButton("Записаться на пробное занятие👍",
	# 											   url="https://docs.google.com/forms/d/1WUwwc9Xiv6LQDQFO6TzvbvvbIqOeVPWqklFxNFvLdKw/edit#response=ACYDBNi7m9BjZI-7ySZlWst-bQTnELpAx7AyfUwqjGWh_225xIw_aZVdLbmofDa2XIdodbk"))
	# 	await bot.edit_message_text(text, query.message.chat.id, query.message.message_id, parse_mode="html", reply_markup=keyboard_markup)
	# else:
	await bot.edit_message_text(text, query.message.chat.id, query.message.message_id, parse_mode="html")


async def text_create(schedule, day_name):
	week = ""
	if day_name == "Неделя":
		for dayweek in schedule:
			if dayweek['day_of_week'] not in week:
				full_text = ""
				date_info = f"🌅{dayweek['day_of_week']}({dayweek['date']})\n"
				for day in schedule:
					if day['day_of_week'] == dayweek['day_of_week']:
						text = (f"\n{' ':6}🕙Время: {day['time']}\n{' ':6}🗺Место: {day['place']}\n")
						full_text = full_text + "    " + text
				week += date_info + full_text + "\n"
		return "<b>" + week + "</b>"
	else:
		full_text = ""
		date_info = f"<b>🏞{schedule[0]['day_of_week']}({schedule[0]['date']})\n"
		for day in schedule:
			text = (f"\n{' ':6}🕙Время: {day['time']}\n{' ':6}🗺Место: {day['place']}\n")
			full_text = full_text + text
		return date_info + full_text + "</b>"

