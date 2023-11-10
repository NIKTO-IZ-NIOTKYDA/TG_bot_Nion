import sqlite3
from time import sleep
from datetime import datetime

import config
from loging import loging

def db_connect():
    loging(logger_level='INFO', user_id='none', do='Connecting to db . . .')
    sleep(1)
    global conn
    conn = sqlite3.connect(config.name_database, check_same_thread=False)
    loging(logger_level='INFO', user_id='none', do='Create a course . . .')
    sleep(1)
    global cursor
    cursor = conn.cursor()

def replace_dz(user_id: int, lesson: str, dz: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing D/Z \'{lesson}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 1'.format(lesson), (dz,))

def replace_photo(user_id: int, path: str, dz: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing photo \'{path}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 2'.format(dz), (path,))

def return_dz(user_id: int, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do='Returning D/Z . . .')
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 1')
    return [str(dz[0]) for dz in cursor.fetchall()]

def return_photo(user_id: int, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do='Search by db photo . . .')
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 2')
    return [str(photo[0]) for photo in cursor.fetchall()]

def return_all_user_id():
    cursor.execute('SELECT user_id FROM users')
    return [str(user_id[0]) for user_id in cursor.fetchall()]

def remove_user_id(user_id: int):
    loging(logger_level='WARN', user_id=str(user_id), do='Deleting an entry in db . . .')
    cursor.execute('DELETE FROM users WHERE user_id = ' + str(user_id))
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def db_add_data(user_id: int, username: str, user_phone_number: str, user_name: str, user_surname: str, user_lang: str):
    loging(logger_level='INFO', user_id=str(user_id), do='Adding data to db . . .')
    cursor.execute('INSERT OR REPLACE INTO users (user_id, username, user_phone_number, user_name, user_surname, user_lang, latest_posts_time) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, username, user_phone_number, user_name, user_surname, user_lang, datetime.now().strftime('%H:%M:%S')))
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def update_latest_posts_time(user_id: int):
    if user_id == config.admin_id_1 or user_id == config.admin_id_2 or user_id == config.admin_id_3:
        pass
    else:
        loging(logger_level='INFO', user_id=str(user_id), do='Update `latest_posts_time` in db . . .')
        cursor.execute('UPDATE users SET latest_posts_time = ? WHERE user_id = ?', (datetime.now().strftime('%H:%M:%S'), user_id))
        loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
        conn.commit()

def return_user_authentication(user_id: int):
    if user_id == config.admin_id_1 or user_id == config.admin_id_2 or user_id == config.admin_id_3:
        return '0'
    else:
        loging(logger_level='INFO', user_id=str(user_id), do='Search by db user_id . . .')
        cursor.execute('SELECT user_id FROM users WHERE user_id = ' + str(user_id))
        if str(cursor.fetchone()) != 'None':
            loging(logger_level='INFO', user_id=str(user_id), do='Successfully !')
            loging(logger_level='INFO', user_id=str(user_id), do='Return 0')
            return '0'
        else:
            loging(logger_level='WARN', user_id=str(user_id), do='Unsuccessfully !')
            loging(logger_level='INFO', user_id=str(user_id), do='Return 1')
            return '1'

def db_backup():
    with open('sql_damp.txt', 'w') as f:
        for sql in conn.iterdump():
            f.write(sql)

def db_stop(user_id: int):
    loging(logger_level='WARN', user_id=str(user_id), do='Admin will reboot the bot . . .')
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()
    loging(logger_level='WARN', user_id=str(user_id), do='Disconnect from db . . .')
    conn.close()
    loging(logger_level='INFO', user_id=str(user_id), do='Successfully !')
    loging(logger_level='WARN', user_id=str(user_id), do='Rebooting . . .')
