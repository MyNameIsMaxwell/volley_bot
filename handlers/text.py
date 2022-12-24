from aiogram import types
from handlers import *

from loader import dp

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
   if msg.text.startswith("Расписание"):
       await schedule.start_cmd_handler(msg)
   elif msg.text.startswith("Помощь"):
        await help.help_command(msg)
   elif msg.text.lower() == 'привет':
       await msg.answer('Привет!')
   else:
       await msg.answer('A?')