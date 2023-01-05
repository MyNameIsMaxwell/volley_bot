import asyncio
from aiogram import types
from aiogram.types import ChatActions
from loguru import logger

from loader import bot, dp
from . import menu
from database import datawork
from states.new_states import GreetingsStates


@dp.message_handler(commands=['start'])
@logger.catch()
async def send_welcome(message: types.Message):
    await message.reply(f'Привет, {message.from_user.first_name}👋\nДумаю, ты зашел сюда неспроста🤗\nИ прежде чем продолжить, ответь, пожалуйста, на <b>важный</b> вопрос: <em>Заряжает ли тебя <b>такая</b> атмосфера?</em>👇', parse_mode="html")
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    btns_text = ('Мне интересно!🤩', 'Не очень🫤')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    volley_preview = 'BAACAgIAAxkDAAIFumO0q3u-Apjr9TcW96lztRxbE1UtAAKaJQACp2-gSeIMdWO_IrOPLQQ'
    await bot.send_chat_action(message.chat.id, action=ChatActions.UPLOAD_VIDEO)
    await asyncio.sleep(3)
    await bot.send_video(message.chat.id,
                         video=volley_preview,
                         reply_markup=keyboard_markup)


@dp.message_handler(text='Мне интересно!🤩')
@dp.message_handler(text='Хорошо! Что там у вас?')
@dp.message_handler(lambda message: message.text.startswith('Лааадно'))
async def greetings_answer(message: types.Message):
    await message.answer(f'<b>Отлично!</b> Тогда..', parse_mode="html")
    # await msg.reply(f'Привет, {msg.from_user.first_name}👋 Я BrestVolleybot. От меня ты можешь узнать расписание тренировок на неделю, либо посмотреть материалы, которые помогут тебе лучше принимать, бить и пасовать)')
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btns_text = ('🏐Открыть меню🏐')
    keyboard_markup.add(btns_text)
    greetings_video = 'BAACAgIAAxkBAAIF-mO1THv0I_R3sAdzlGDX_gI_g8JxAALJHwACp2-oST5fmkYUl1jdLQQ'
    await bot.send_video(message.chat.id,
                         video=greetings_video,
                         reply_markup=keyboard_markup)


@dp.message_handler(text='Не очень🫤')
async def ungreetings_answer(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btns_text = ('Хорошо! Что там у вас?', 'Все равно нет!')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    volley_preview = 'BAACAgIAAxkDAAIFumO0q3u-Apjr9TcW96lztRxbE1UtAAKaJQACp2-gSeIMdWO_IrOPLQQ'
    await message.reply_video(
                         video=volley_preview,
                         caption='А может посмотри видео еще разок😅',
                         reply_markup=keyboard_markup)

@dp.message_handler(text='Все равно нет!')
async def absolutely_no(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btns_text = ('Лааадно, я передумал)')
    keyboard_markup.add(btns_text)
    sad_sticker_id = 'CAACAgIAAxkBAAEHHnRjtVPjB5BM2GLxSqTkDT-Hzr0ZWQACNwUAAiMFDQABV0mQXjjUSrEtBA'
    await message.answer("Жаль, что тебе не понравилось..")
    await message.answer_sticker(sad_sticker_id, reply_markup=keyboard_markup)

@dp.message_handler(text='🏐Открыть меню🏐')
async def greetings_answer(message: types.Message):
    await message.reply(f'Еще раз привет✋ Я BrestVolleybot. От меня ты можешь узнать расписание тренировок на неделю, либо посмотреть материалы, которые помогут тебе лучше принимать, бить и пасовать)')
    await datawork.add_user(message)
    await menu.menu_cmd(message)
