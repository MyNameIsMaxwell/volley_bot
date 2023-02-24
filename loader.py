from aiogram import Bot, Dispatcher, types
from loguru import logger
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_data import config
from database import datawork
from get_user_info import google_sheet_parse
from states.new_states import GreetingsStates

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()


async def training_feedback(users_id, training_info):
   if users_id:
      text = "Понравилась пробная тренировка?😇"
      keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
      btns_text = ('Да! Было здорово😎', 'Нет! Скучно😤')
      keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
      # text = "И снова здравствуйте!🙌\n\nЖдем Вас на пробной тренировке\n\nСтоимость пробной тренировки - 10 рублей.\n\nРекомендуем взять с собой:\n\n1) спортивную форму\n2) сменную обувь\n3) бутылку с водой\n4) полотенце\n5) хорошее настроение!😀\n\nЕсли возникнут вопросы - свяжитесь с нами\n\nДо встречи на тренировке!😉"
      # # Добавить считывание дня тренировки
      for id_value in users_id:
         await bot.send_message(id_value, text, reply_markup=keyboard_markup)
   if training_info:
      locations_info = await datawork.locations_get(training_info['date'][2])
      try:
         for location in locations_info:
            address = location['street_name']
            name = location['name']
            map_location = location['map_location']
      except Exception as exp:
         print(exp)
         address = '(Наберите для уточнения)'
         name="Пожалуйста:)"
      text = "И снова здравствуйте!🙌\n\nЖдем Вас на пробной тренировке {date} числа в {time} по адресу {location}({name})💪\n\nСтоимость пробной тренировки - 10 рублей.\n\nРекомендуем взять с собой:\n\n1) спортивную форму\n2) сменную обувь\n3) бутылку с водой\n4) полотенце\n5) хорошее настроение!😀\n\nЕсли возникнут вопросы - свяжитесь с нами\n\nДо встречи на тренировке!😉".format(
         date=training_info['date'][0] + ' ' + training_info['date'][1],
         time=training_info['date'][3],
         location=address,
         name=name
      )
      keyboard_markup = types.InlineKeyboardMarkup()
      keyboard_markup.add(types.InlineKeyboardButton('Показать на карте', url=f"{map_location}"))
      await bot.send_message(training_info['user'], text, reply_markup=keyboard_markup)

      # await GreetingsStates.training_interest.set()


async def check_situation():
   google_sheet_parse.changes_check()
   await google_sheet_parse.training_status_true()

logger.add(config.LOG_PATH, format="{time} - {level} - {message}", level="DEBUG", rotation="10 MB", compression="zip")
# job = scheduler.add_job(check_situation, 'interval', minutes=60)
job = scheduler.add_job(check_situation, 'interval', seconds=30)