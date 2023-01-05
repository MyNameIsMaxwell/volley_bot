from aiogram import types
from handlers import *

from loader import dp


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.text.startswith("Расписание"):
        await schedule.start_schedule_handler(msg)
    elif msg.text.startswith("Записаться на"):
        await trial_lesson.trial_lesson_handler(msg)
    elif msg.text.startswith("О нас"):
        await about_us.about_us_handler(msg)
    elif msg.text.startswith("Помощь"):
        await help.help_command(msg)
    elif msg.text.startswith("Прайс"):
        await price_list.price_list_handler(msg)
    elif msg.text.lower() == 'привет':
        await msg.answer('Привет!')
    else:
        await msg.answer('Пока что дальше этих /help команд я не понимаю🤷‍♂️')
