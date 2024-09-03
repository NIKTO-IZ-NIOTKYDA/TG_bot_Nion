import sqlite3
from typing import Any

from base64 import b64encode, b64decode

import loging
import colors_log
import encryption
from config import name_database, debug

log = loging.logging(Name='DB', Color=colors_log.yellow)


def db_connect() -> None:
    log.info(user_id=None, msg='Connecting to db . . .')
    global conn
    conn = sqlite3.connect(name_database, check_same_thread=False)
    log.info(user_id=None, msg='Create a course . . .')
    global cursor
    cursor = conn.cursor()


# Setting
def set_dz(user_id: int, lesson: str, dz: str) -> None:
    log.info(user_id=str(user_id), msg=f'Setting D/Z \'{lesson}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 1'.format(lesson), [dz])
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()
    return


def set_photo(user_id: int, path: str, lesson: str) -> None:
    log.info(user_id=str(user_id), msg=f'Setting photo \'{path}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 2'.format(lesson), [path])
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()


def set_url(user_id: int, url: str, lesson: str) -> None:
    log.info(user_id=str(user_id), msg=f'Setting url \'{url}\'')
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 3'.format(lesson), [url])
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()


def set_send_notifications(user_id: int, send_notifications: bool) -> None:
    log.info(user_id=str(user_id), msg=f'Setting send_notifications \'{send_notifications}\'')
    cursor.execute('UPDATE users SET send_notifications = ? WHERE user_id = ?', [send_notifications, user_id])
    
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()


def set_net_school(user_id: int, login: str, password: str, key: str) -> None:
    log.info(user_id=str(user_id), msg='Encrypting login and password . . .')
    b64_login = b64encode(login.encode('utf-8'))
    b64_key = b64encode(key.encode('utf-8'))
    aes256_password = encryption.encrypt(password, key)

    log.info(user_id=str(user_id), msg='Setting in NetSchool login and password . . .')
    cursor.execute('INSERT OR REPLACE INTO net_school (user_id, enc_login, enc_password, enc_key) VALUES (?, ?, ?, ?)',
                   (user_id, b64_login, aes256_password, b64_key))

    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()


###########################################################


# Gets
def get_dz(user_id: int, lesson: str) -> str:
    log.info(user_id=str(user_id), msg='Getting D/Z . . .')
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 1')
    return cursor.fetchall()[0][0]


def get_photo(user_id: int, lesson: str) -> str:
    log.info(user_id=str(user_id), msg='Search by db photo . . .')
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 2')
    return cursor.fetchall()[0][0]


def get_url(user_id: int, lesson: str) -> str:
    log.info(user_id=str(user_id), msg='Search by db url . . .')
    cursor.execute(f'SELECT {lesson} FROM dz WHERE id = 3')
    return cursor.fetchall()[0][0]


def get_send_notifications(user_id: int) -> bool | None:
    log.info(user_id=str(user_id), msg='Search by db send_notifications . . .')
    cursor.execute('SELECT send_notifications FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchone()
    if result != None:
        return result[0]  # type: ignore
    else:
        return None


def get_net_school(user_id: int, decode: bool = True) -> dict[str] | bool | KeyError | None:
    log.info(user_id=str(user_id), msg='Getting login and password from NetSchool . . .')
    cursor.execute('SELECT * FROM net_school WHERE user_id = ?', [user_id])
    try:
        result = cursor.fetchall()[0]
    except IndexError:
        log.info(user_id=str(user_id), msg='Incorrect user_id')
        return None
    
    if not decode:
        return True
    else:
        try:
            dict = {
                'login': b64decode(result[1]).decode('utf-8'),
                'password': encryption.decrypt(encrypted_password=result[2], key=b64decode(result[3]).decode('utf-8')),
                'key': b64decode(result[3]).decode('utf-8')
            }

        except Exception:
            log.info(user_id=str(user_id), msg='Incorrect key')
            return KeyError
        return dict


def get_user_id(user_id: int) -> Any:
    log.info(user_id=str(user_id), msg='Getting users . . .')
    cursor.execute(f'SELECT * FROM users WHERE user_id = ?', [user_id])
    return cursor.fetchone()


def get_all_user_id(user_id: int, auto: bool) -> list[int] | None:
    log.info(user_id=str(user_id), msg='Getting all users . . .')
    if auto:
        cursor.execute('SELECT user_id FROM users WHERE send_notifications = 1')
    else:
        cursor.execute('SELECT user_id FROM users')
    result = cursor.fetchall()
    if result != None:
        return result[0]
    else:
        return None


def get_user_authentication(user_id: int) -> bool:
    log.info(user_id=str(user_id), msg='Search by db user_id . . .')
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', [user_id])
    if str(cursor.fetchone()) != 'None':
        return True
    else:
        return False


###########################################################


def db_add_data(user_id: int, username: str, user_name: str, user_surname: str, user_lang: str) -> None:
    log.info(user_id=str(user_id), msg='Adding data to db . . .')
    gsn = get_send_notifications(user_id=user_id)
    if gsn != None:
        cursor.execute('INSERT OR REPLACE INTO users (user_id, username, user_name, user_surname, user_lang, send_notifications) VALUES (?, ?, ?, ?, ?, ?)', [user_id, username, user_name, user_surname, user_lang, gsn])
    else:
        cursor.execute('INSERT OR REPLACE INTO users (user_id, username, user_name, user_surname, user_lang, send_notifications) VALUES (?, ?, ?, ?, ?, ?)', [user_id, username, user_name, user_surname, user_lang, True])
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()


def remove_user(user_id: int) -> None:
    log.warn(user_id=str(user_id), msg='Deleting an entry in db . . .')
    cursor.execute('DELETE FROM users WHERE user_id = ?', [user_id])
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()


def db_stop(user_id: int) -> None:
    log.warn(user_id=str(user_id), msg='Stoping . . .')
    log.debug(user_id=str(user_id), msg='Saving data to db . . .')
    conn.commit()
    log.warn(user_id=str(user_id), msg='Disconnect from db . . .')
    conn.close()
    log.info(user_id=str(user_id), msg='Successfully !')


db_connect()
