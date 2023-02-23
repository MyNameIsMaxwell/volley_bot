import os
import re

import httplib2
import apiclient.discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

import loader
from config_data.config import SPREADSHEET_ID
# from handlers import sender


# Файл, полученный в Google Developer Console
if __name__ == '__main__':
    CREDENTIALS_FILE = os.path.abspath(os.path.join('client_secret.json'))
else:
    CREDENTIALS_FILE = os.path.abspath(os.path.join('get_user_info/client_secret.json'))
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = SPREADSHEET_ID

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_newbie_users_info() -> list:
    """
    Функция чтения информации из таблицы
    """
    try:
        range_names = ['Новички!F2:F300', 'Новички!C2:C300', 'Новички!D2:D300', 'Новички!E2:E300', 'Новички!B2:B300', 'Новички!G2:G300']
        values = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=range_names,
            majorDimension='COLUMNS'
        ).execute()
        user_id = values['valueRanges'][0]['values'][0]
        form_status = values['valueRanges'][1]['values'][0]
        training_status = values['valueRanges'][2]['values'][0]
        subscription = values['valueRanges'][3]['values'][0]
        names = values['valueRanges'][4]['values'][0]
        usernames = values['valueRanges'][5]['values'][0]
        return user_id, form_status, training_status, subscription, names, usernames
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def training_date_time_get(date):
    try:
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='Расписание!B1:H4',
            majorDimension='COLUMNS'
        ).execute()
        place_id = values['values']
        print(place_id)
        # return place_id
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


training_date_time_get(23)


def get_non_active_users():
    """
    Функция получения списка id аккаунтов, которые не заполнили анкету
    """
    no_form_users = []
    user_id, form_status, training_status, subscription, names, usernames = get_newbie_users_info()
    for index in range(0, len(user_id)):
        if form_status[index] == '0' or training_status[index] == '0':
            no_form_users.append(user_id[index])
    return no_form_users


def check_last_id(table_name):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{table_name}!A1:A300',
        majorDimension='COLUMNS'
    ).execute()

    last_id = values['values'][0][-1]
    last_index = len(values['values'][0])
    return last_id, last_index


def add_new_user(ids_info: list) -> None:
    """
    Функция записи информации об пользователе в таблицу.
    :param ids_info: list с информацией о пользователе
    """
    try:
        last_id = int(check_last_id('Новички')[0]) + 2
        last_index = int(check_last_id('Новички')[1]) + 1
        values = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"Новички!A{last_id}:G{last_id}",
                     "values": [[last_id-1, ids_info[0], '0', '0', '0', ids_info[1], ids_info[2]]]}
                    ]
            }
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def user_position(user_id_value):
    user_id, form_status, training_status, subscription, names, usernames = get_newbie_users_info()
    try:
        return user_id.index(user_id_value)
    except Exception as exp:
        print(exp)


def trial_training_edit(index, status_index):
    try:
        if status_index == '1':
            values = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"Новички!D{index + 2}",
                valueInputOption="USER_ENTERED",
                body={
                        "values": [['2']],
                    }
            ).execute()
        elif status_index == '2':
            values = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"Новички!D{index + 2}",
                valueInputOption="USER_ENTERED",
                body={
                    "values": [['3']],
                }
            ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


async def training_status_true():
    user_id, form_status, training_status, subscription, names, usernames = get_newbie_users_info()
    users_training_done = set()
    users_training_go = set()
    for index in range(0, len(user_id)):
        if training_status[index] == '2':
            users_training_done.add(int(user_id[index]))
            trial_training_edit(index, '2')
        if form_status[index] != '0' and training_status[index] == '0':
            training_place = training_date_time_get(index)
    return await loader.training_feedback(users_training_done)


def changes_check():
    user_id, form_status, training_status, subscription, names, usernames = get_newbie_users_info()
    user_info = []
    try:
        for index in range(0, len(user_id)):
            if subscription[index] == '1':
                row = user_position(user_id[index])
                user_info.append(names[index])
                user_info.append(user_id[index])
                user_info.append(usernames[index])
                user_add_to_club(user_info)
                delete_new_user(row)
            elif training_status[index] == '1':
                trial_training_edit(index, '1')
    except IndexError:
        return


def delete_new_user(row_num):
    row_num = int(row_num) + 1
    row_value = int(row_num) + 1
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [{
                    'deleteRange': {
                        # f"Новички!A{row_value}:F{row_value}"
                        "range": {"sheetId": 1755001043,
                                  "startRowIndex": row_num,
                                  "endRowIndex": row_value,
                                  "startColumnIndex": 0,
                                  "endColumnIndex": 7},
                        "shiftDimension": "ROWS"
                    }
                }]
            }
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def user_add_to_club(user_info):
    """
        Функция записи информации об пользователе в таблицу.
        :param user_info: list с информацией о пользователе
        """
    try:
        last_id = int(check_last_id('Клуб')[0]) + 2
        values = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": f"Клуб!A{last_id}:B{last_id}",
                        "values": [[last_id - 1, user_info[0]]]
                     },
                    {
                        "range": f"Клуб!G{last_id}:H{last_id}",
                        "values": [[user_info[1], user_info[2]]]
                     },
                ]
            }
        ).execute()
        user_info.clear()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
