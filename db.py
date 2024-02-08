import sqlite3

import config
from loging import loging, debug

def db_connect():
    loging(logger_level='INFO', user_id='none', do='Connecting to db . . .')
    global conn
    conn = sqlite3.connect(config.name_database, check_same_thread=False)
    loging(logger_level='INFO', user_id='none', do='Create a course . . .')
    global cursor
    cursor = conn.cursor()

def replace_dz(user_id: int, lesson: str, dz: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing D/Z \'{lesson}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 1'.format(lesson), (dz,))
    if debug:
        loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def replace_photo(user_id: int, path: str, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing photo \'{path}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 2'.format(lesson), (path,))
    if debug:
        loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def replace_url(user_id: int, url: str, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing url \'{url}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 3'.format(lesson), (url,))
    if debug:
        loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def return_dz(user_id: int, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do='Returning D/Z . . .')
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 1')
    return [str(dz[0]) for dz in cursor.fetchall()]

def return_photo(user_id: int, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do='Search by db photo . . .')
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 2')
    return [str(photo[0]) for photo in cursor.fetchall()]

def return_url(user_id: int, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do='Search by db url . . .')
    cursor.execute(f'SELECT {lesson} FROM dz WHERE id = 3')
    return [str(url[0]) for url in cursor.fetchall()]

def return_all_user_id(user_id: int):
    loging(logger_level='INFO', user_id=str(user_id), do='Returning all users . . .')
    cursor.execute('SELECT user_id FROM users')
    return [str(user_id[0]) for user_id in cursor.fetchall()]

def remove_user(user_id: int):
    loging(logger_level='WARN', user_id=str(user_id), do='Deleting an entry in db . . .')
    cursor.execute('DELETE FROM users WHERE user_id = ' + str(user_id))
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def db_add_data(user_id: int, username: str, user_name: str, user_surname: str, user_lang: str):
    if debug:
        loging(logger_level='INFO', user_id=str(user_id), do='Adding data to db . . .')
    cursor.execute('INSERT OR REPLACE INTO users (user_id, username, user_name, user_surname, user_lang) VALUES (?, ?, ?, ?, ?)', (user_id, username, user_name, user_surname, user_lang))
    if debug:
        loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def return_user_authentication(user_id: int):
    if user_id == config.main_admin_id:
        return 0
    else:
        if debug:
            loging(logger_level='INFO', user_id=str(user_id), do='Search by db user_id . . .')
        cursor.execute('SELECT user_id FROM users WHERE user_id = ' + str(user_id))
        if str(cursor.fetchone()) != 'None':
            return 0
        else:
            return 1

def db_stop(user_id: int):
    loging(logger_level='WARN', user_id=str(user_id), do='Admin will reboot the bot . . .')
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()
    loging(logger_level='WARN', user_id=str(user_id), do='Disconnect from db . . .')
    conn.close()
    loging(logger_level='INFO', user_id=str(user_id), do='Successfully !')
    loging(logger_level='WARN', user_id=str(user_id), do='Rebooting . . .')
