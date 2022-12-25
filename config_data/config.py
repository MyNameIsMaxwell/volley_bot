import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv('.env.template'):
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv('.env.template')

BOT_TOKEN = os.getenv('BOT_TOKEN')

DEFAULT_COMMANDS = (
    ('schedule', "Расписание тренировок на неделю📆"),
    ('coaches', "Наши тренера🧙"),
    ('gyms_location', "Месторасположение залов🗺"),
    ('price_list', "Прайс-лист💸"),
    ('help', "Вывести справку🏐")
)
LOG_PATH = os.path.abspath(os.path.join('utils', 'logs.log'))