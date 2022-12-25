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

class Location(Model):
    short_name = CharField()
    street = CharField(null=False)
    photo = CharField(null=False)
    map_location_url = CharField(null=False)

    class Meta:
        database = datab

class Coach(Model):
    name = CharField(null=False)
    photo = CharField(null=False)
    descr = TextField(null=False)

    class Meta:
        database = datab

class Price(Model):
    name = CharField(null=False)
    photo = CharField(null=False)
    descr = TextField(null=False)

    class Meta:
        database = datab

cur = datab.cursor()

def create_tables():
    Users.create_table()
    Schedule.create_table()
    Location.create_table()
    Coach.create_table()

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

async def locations_get(id_value=0):
    locations_list = []
    if id_value:
        location_info = Location.select().where(Location.id == id_value)
    else:
        location_info = Location.select()
    for location in location_info:
        location_dict = {}
        location_dict["id"] = location.id
        location_dict["name"] = location.short_name
        location_dict["street_name"] = location.street
        location_dict["photo"] = location.photo
        location_dict["map_location"] = location.map_location_url
        locations_list.append(location_dict)
    return locations_list

def coaches_get():
    coaches_list = []
    coaches_info = Coach.select()
    for coach in coaches_info:
        coaches_dict = {}
        coaches_dict["id"] = coach.id
        coaches_dict["name"] = coach.name
        coaches_dict["photo"] = coach.photo
        coaches_dict["description"] = coach.descr
        coaches_list.append(coaches_dict)
    return coaches_list

