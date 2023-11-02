import sqlite3
from time import sleep

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

def return_all_user_id():
    cursor.execute(f'SELECT user_id FROM users')
    return cursor.fetchone()

def remove_user_id(user_id: str):
    loging(logger_level='WARN', user_id=f'{user_id}', do='Deleting an entry in db . . .')
    cursor.execute(f'DELETE from users where user_id = ' + user_id)
    loging(logger_level='INFO', user_id=f'{user_id}', do='Saving data to db . . .')
    conn.commit()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str,  user_lang: str, user_phone_number: str):
    loging(logger_level='INFO', user_id=f'{user_id}', do='Adding data to db . . .')
    cursor.execute('INSERT OR REPLACE INTO users (user_id, user_name, user_surname, username, user_lang, user_phone_number, user_authentication) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, user_lang, user_phone_number, 1))
    conn.commit()

def db_table_bool_return(user_id: int):
    loging(logger_level='INFO', user_id=f'{user_id}', do='Search by db user_id . . .')
    cursor.execute('SELECT user_authentication FROM users WHERE user_id = ' + str(user_id))
    return str(cursor.fetchone())


def db_backup():
    with open('sql_damp.txt', 'w') as f:
        for sql in conn.iterdump():
            f.write(sql)

def db_stop(user_id: str):
    loging(logger_level='WARN', user_id=f'{user_id}', do='Admin will reboot the bot . . .')
    loging(logger_level='INFO', user_id=f'{user_id}', do='Saving data to db . . .')
    conn.commit()
    loging(logger_level='WARN', user_id=f'{user_id}', do='Disconnect from db . . .')
    conn.close()
    loging(logger_level='INFO', user_id=f'{user_id}', do='Successfully !')
    loging(logger_level='WARN', user_id=f'{user_id}', do='Rebooting . . .')
