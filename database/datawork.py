import os
from peewee import *
from loguru import logger

if __name__ != '__main__':
    datab = SqliteDatabase(os.path.abspath(os.path.join('./database/voley_db.db')))
else:
    datab = SqliteDatabase(os.path.abspath(os.path.join('./voley_db.db')))

class Users(Model):
    id = IntegerField(null=False, primary_key=True)
    user_id = IntegerField(null=False, unique=True)
    user_name = CharField()

    class Meta:
        database = datab

class Schedule(Model):
    week_day = CharField(null=False)
    day = IntegerField(null=False)
    month = IntegerField(null=False)
    year = IntegerField(null=False)
    time = TimeField()
    place = CharField(null=False)

    class Meta:
        database = datab

cur = datab.cursor()

def create_tables():
    Users.create_table()
    Schedule.create_table()

@logger.catch()
async def add_user(message):
    try:
        user_exist = cur.execute("""SELECT id FROM users
        									WHERE user_id = ?""", (message.from_user.id,)).fetchone()
        if user_exist == None:
            Users.create(user_id=message.from_user.id,
                         user_name=f"{message.from_user.username} - {message.from_user.first_name} {message.from_user.last_name}"
                        )
    except Exception as exp:
        if str(exp) != "no such table: users":
            print(exp)

async def schedule_get(week_day_value):
    schedule_list = []
    if week_day_value == "Неделя":
        date = Schedule.select()
    else:
        date = Schedule.select().where(Schedule.week_day == week_day_value)
    for schedule_info in date:
        day_info = {}
        day_info['day_of_week'] = schedule_info.week_day
        day = schedule_info.day
        month = schedule_info.month
        year = schedule_info.year
        day_info['date'] = f"{day}.{month}.{year}"
        if (schedule_info.time.minute) != 0:
            day_info['time'] = f"{str(schedule_info.time.hour)}:{str(schedule_info.time.minute)}"
        else:
            day_info['time'] = f"{str(schedule_info.time.hour)}:00"
        day_info['place'] = schedule_info.place
        schedule_list.append(day_info)
    return schedule_list