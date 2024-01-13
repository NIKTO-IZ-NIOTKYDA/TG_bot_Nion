import sqlite3
from datetime import datetime

import config
from loging import loging

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
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def replace_photo(user_id: int, path: str, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing photo \'{path}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 2'.format(lesson), (path,))
    loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
    conn.commit()

def replace_url(user_id: int, url: str, lesson: str):
    loging(logger_level='INFO', user_id=str(user_id), do=f'Replaceing url \'{url}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 3'.format(lesson), (url,))
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

def return_all_user_id():
    cursor.execute('SELECT user_id FROM users')
    return [str(user_id[0]) for user_id in cursor.fetchall()]

def remove_user(user_id: int):
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
    if user_id == config.main_admin_id:
        pass
    else:
        loging(logger_level='INFO', user_id=str(user_id), do='Update `latest_posts_time` in db . . .')
        cursor.execute('UPDATE users SET latest_posts_time = ? WHERE user_id = ?', (datetime.now().strftime('%H:%M:%S'), user_id))
        loging(logger_level='INFO', user_id=str(user_id), do='Saving data to db . . .')
        conn.commit()

def return_user_authentication(user_id: int):
    if user_id == config.main_admin_id:
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
