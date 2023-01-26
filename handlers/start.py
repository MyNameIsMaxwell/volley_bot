import asyncio
from aiogram import types
from aiogram.types import ChatActions
from aiogram.dispatcher.filters import state
from loguru import logger

from loader import bot, dp
from . import menu, first_connection
from database import datawork
from states.new_states import GreetingsStates


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    btns_text = ('Да!🎒', 'Нет💼')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    await message.reply(f'Привет, {message.from_user.first_name}, и добро пожаловать в команду Brest Volley!🔥🙌\n\nРады видеть тебя в рядах нашего волейбольного клуба и школы волейбола!🏆🏐\n\nBrest Volley - это Клуб, объединяющий профессионалов и любителей волейбола в одно большое комьюнити!\n\nПрофессиональный подход, квалифицированные тренеры, видеоанализ техники и много другое ждет Вас в волейбольном клубе «Brest Volley»! 🔥🏆🥇\n\nРазминочный вопрос: Ты еще учишься в школе?',
                        parse_mode="html",
                        reply_markup=keyboard_markup)


@dp.message_handler(text='Нет💼')
@logger.catch()
async def send_video(message: types.Message):
    await datawork.add_user(message)
    await datawork.worker_change(message)
    await message.reply(f'Тогда вопрос посерьезнее: <em>Заряжает ли тебя <b>такая</b> атмосфера?</em>👇', parse_mode="html")
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    btns_text = ('Мне интересно!🤩', 'Не очень🫤')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    volley_preview = 'BAACAgIAAxkDAAIFumO0q3u-Apjr9TcW96lztRxbE1UtAAKaJQACp2-gSeIMdWO_IrOPLQQ'
    await bot.send_chat_action(message.chat.id, action=ChatActions.UPLOAD_VIDEO)
    await asyncio.sleep(2)
    await bot.send_video(message.chat.id,
                         video=volley_preview,
                         reply_markup=keyboard_markup)


@dp.message_handler(text='Да!🎒')
@logger.catch()
async def send_video(message: types.Message):
    await datawork.add_user(message)
    await datawork.schooler_change(message)
    await message.reply(f'Тогда вопрос посерьезнее: <em>Заряжает ли тебя <b>такая</b> атмосфера?</em>👇', parse_mode="html")
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    btns_text = ('Мне интересно!🤩', 'Не очень🫤')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    volley_preview = 'BAACAgIAAxkBAAIIgWO8nMK1wF9B7T6QV1CywIY7eBdPAAI9KgACW9LpSbwgjFKLDxfuLQQ'
    await bot.send_chat_action(message.chat.id, action=ChatActions.UPLOAD_VIDEO)
    await asyncio.sleep(2)
    await bot.send_video(message.chat.id,
                         video=volley_preview,
                         reply_markup=keyboard_markup)


@dp.message_handler(text='Мне интересно!🤩')
@dp.message_handler(text='Хорошо! Что там у вас?')
@dp.message_handler(lambda message: message.text.startswith('Лааадно'))
async def greetings_answer(message: types.Message):
    await message.answer(f'<b>Отлично!</b> Тогда..', parse_mode="html")
    # await msg.reply(f'Привет, {msg.from_user.first_name}👋 Я BrestVolleybot. От меня ты можешь узнать расписание тренировок на неделю, либо посмотреть материалы, которые помогут тебе лучше принимать, бить и пасовать)')
    if await datawork.get_user_status(message) is True:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
        btns_text = ('Записаться на пробное!😍', 'Хочу узнать больше!')
        keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    else:
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
    if await datawork.schooler_get(message) == 0:
        volley_preview = 'BAACAgIAAxkDAAIFumO0q3u-Apjr9TcW96lztRxbE1UtAAKaJQACp2-gSeIMdWO_IrOPLQQ'
    else:
        volley_preview = 'BAACAgIAAxkBAAIIgWO8nMK1wF9B7T6QV1CywIY7eBdPAAI9KgACW9LpSbwgjFKLDxfuLQQ'
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
    await menu.menu_cmd(message)


@dp.message_handler(text='Хочу узнать больше!')
async def greetings_answer(message: types.Message):
    await message.reply(f'Еще раз привет✋ Я BrestVolleybot. От меня ты можешь узнать расписание тренировок на неделю, либо посмотреть материалы, которые помогут тебе лучше принимать, бить и пасовать)')
    await menu.menu_cmd(message)