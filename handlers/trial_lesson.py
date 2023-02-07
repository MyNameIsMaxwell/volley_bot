from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers import about_us, start
from loader import bot, dp
from states.new_states import GreetingsStates


@dp.message_handler(commands=["trial_lesson"])
async def trial_lesson_handler(message: types.Message):
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(types.InlineKeyboardButton("Записаться на тренировку👍",
												   url="https://docs.google.com/forms/d/1WUwwc9Xiv6LQDQFO6TzvbvvbIqOeVPWqklFxNFvLdKw/edit#response=ACYDBNi7m9BjZI-7ySZlWst-bQTnELpAx7AyfUwqjGWh_225xIw_aZVdLbmofDa2XIdodbk"))
	await bot.send_message(message.chat.id, "<em>Если хотите добиться успеха, задайте себе 4 вопроса: Почему? А почему бы и нет? Почему бы и не я? Почему бы и не прямо сейчас?</em>",
							parse_mode="html",
							reply_markup=keyboard_markup
						   )


@dp.message_handler(text="Да! Было здорово😎")
@dp.message_handler(text="Нет! Скучно😤")
async def training_interest_handler(message: types.Message):
	if message.text.startswith('Да'):
		keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
		btn_text = ("Хочу в Клуб!✌️", "Пока не готов🙁")
		keyboard_markup.row(*(types.KeyboardButton(btn) for btn in btn_text))
		text = "Тогда вступай в Клуб!\n\nВступив в клуб ты получишь:\n\n- тренировки с тренером\n- видеоанализ техники\n- командный чат\n- еженедельный план тренировок\n- клубные мероприятия\n- скидки от партнеров\n- попадешь в сообщество сильных и позитивных людей\n\n \
				И....\n\n1. Разовьёшь новые нейронные связи!\n2. Разовьёшь физические качества и умственные способности!\n3. Обретёшь желаемую физическую форму!\n4. Обретёшь уверенность в себе!\n5. Разовьёшь (усовершенствуешь) коммуникативные навыки и умение работать в команде!\n\
6. Весело и интересно, с удовольствием и пользой проведёшь время!\n7. Найдешь новых знакомых, друзей, а возможно и вторую половинку!\n8. Попадёшь в сообщество сильных и позитивных людей!\n9. Ну и конечно же научишься играть в волейбол, станешь «Королем»/ «Королевой» ПЛЯЖА! И будешь приковывать к себе внимание всех отдыхающих...😉\n\n\
Все вышеперечисленное и не только... ты получишь, став членом нашего Клуба!🏐 👨‍👩‍👧‍👧\n\nВступай в клуб и становись лучшей версией себя вместе с Brest Volley! 💪"
		await GreetingsStates.interest_yes.set()
	elif message.text.startswith('Нет'):
		keyboard_markup = types.InlineKeyboardMarkup()
		keyboard_markup.add(types.InlineKeyboardButton('Записаться на пробное еще раз😁', callback_data="trial_lesson_on"))
		text = "#Небольшой пост\n\nВолейбол - командная игра, в которой одновременно принимает участие много людей.\n\nК сожалению, иногда бывает так, что:\n- кто-то из участников был не в лучшем настроении\n- не нашли коннект с тренером\n- не лучшим образом сложились обстоятельства и т.д...\n\nПоэтому рекомендуем попробовать еще раз!😉\n\nВыберите удобный для себя день.... и запишитесь на тренировку!"
	else:
		text = "Прости, кроме Да или Нет не могу принять😄"

	if 'keyboard_markup' in locals():
		await bot.send_message(message.chat.id, text, reply_markup=keyboard_markup)
	else:
		await bot.send_message(message.from_user.id, text)


@dp.message_handler(state=GreetingsStates.interest_yes)
async def interest_yes_handler(message: types.Message, state: FSMContext):
	if message.text.startswith('Хочу в Клуб'):
		keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
		btn_text = ("Как оплатить️🙌", "Дороговато😵‍💫")
		keyboard_markup.row(*(types.KeyboardButton(btn) for btn in btn_text))
		text = "Варианты Клубных карт👆\n\nСтать членом Клуба и получать все вышеперечисленные ценности ты можешь уплатив символический членский взнос в Клуб (получив Клубную карту)\n\nВсе клубные карты можно приобретать в рассрочку(!), ежемесячно оплачивая равными частями либо любым другим удобным способом.\n\n<i><b>Вступай в клуб и становись лучшей версией себя вместе с Brest Volley! 💪</b></i>"
		photo = types.InputFile(f"img/price_list.png")
		await GreetingsStates.expensive.set()
		await bot.send_photo(message.chat.id, photo=photo, caption=text, parse_mode="html", reply_markup=keyboard_markup)
	elif message.text.startswith('Пока не готов'):
		await start.more_info(message)


@dp.message_handler(state=GreetingsStates.expensive)
async def expensive_handler(message: types.Message, state: FSMContext):
	if message.text.startswith('Как оплатить'):
		text = "Варианты оплаты👇"
	elif message.text.startswith('Дорого'):
		text = 'Пост "Цена и ценность"'
	else:
		text = 'Хм?'
	if text != 'Хм?':
		await state.finish()
	await bot.send_message(message.from_user.id, text)
