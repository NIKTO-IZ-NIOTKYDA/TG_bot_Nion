import os
from re import U
from typing import Any
from time import sleep
from math import gcd

import telebot
from sympy import randprime, primerange

import db
import config
import loging
import colors_log

log = loging.logging(Name='UTILS', Color=colors_log.blue)

num_lessons: int = 19
dict_name_lessons = {
    0: ['algebra', 'Алгебра'],
    1: ['english_lang_1', 'Англ. Яз. (1 группа)'],
    2: ['english_lang_2', 'Англ. Яз. (2 группа)'],
    3: ['biology', 'Биология'],
    4: ['geography', 'География'],
    5: ['geometry', 'Геометрия'],
    6: ['computer_science_1', 'Информатика (1 группа)'],
    7: ['computer_science_2', 'Информатика (2 группа)'],
    8: ['story', 'История'],
    9: ['literature', 'Литература'],
    10: ['music', 'Музыка'],
    11: ['OBZH', 'ОБЖ'],
    12: ['social_science', 'Обществознание'],
    13: ['native_literature', 'Родная литература'],
    14: ['russian_lang', 'Русский язык'],
    15: ['TBIS', 'Теория вероятностей и статистика'],
    16: ['technology', 'Технология'],
    17: ['physics', 'Физика'],
    18: ['chemistry', 'Химия']
}

def rename(user_id: int, file_name_in: str, file_name_out: str) -> None:
    log.info(user_id=str(user_id), msg=f'Rename {file_name_in} -> {file_name_out}')
    try:
        os.system(f'mv {file_name_in} {file_name_out}')
        log.info(user_id=str(user_id), msg='Successfully !')
    except Exception as Error:
        log.error(user_id=str(user_id), msg=str(Error))


def send_status_text(user_id: int, bot: telebot.TeleBot) -> None:
    log.info(user_id=user_id, msg='Call send_status_text')
    # if config.debug:
        # log.info(user_id=str(user_id), msg='Send status . . .')
    # bot.send_chat_action(user_id, action='typing')


def newsletter(user_id: int, text: str, auto: bool, bot: telebot.TeleBot) -> None:
    log.warn(user_id=str(user_id), msg='Start of the mailing')

    all_user_id = db.get_all_user_id(user_id, auto=auto)

    if all_user_id != None:
        timer: int = 0

        for user_id_ in all_user_id:  # type: ignore[union-attr]
            if timer < 29:
                try:
                    bot.send_message(chat_id=user_id_, text=text)
                    log.info(user_id=str(user_id_), msg=f'Sent: {user_id_}')

                    timer += 1
                    continue
                except telebot.apihelper.ApiException as Error:
                    if Error.result.status_code == 403 or Error.result.status_code == 400:
                        log.warn(user_id=str(user_id_), msg=f'User {user_id_} has blocked the bot!')
                        # db.remove_user(user_id=str(user_id_))

                        timer += 1
                        continue
                except Exception as Error:
                    log.error(user_id=str(user_id_), msg=str(Error))

                    timer += 1
                    continue
            else:
                sleep(1.15)
                timer = 0

    log.info(user_id=str(user_id), msg='Mailing is over')
    bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=telebot.types.InlineKeyboardMarkup(row_width=1).add(telebot.types.InlineKeyboardButton(text='⏪ Вернуться в главное меню', callback_data='back_in_main_menu')))
    return


def send_update_dz(user_id: int, lesson: str, bot: telebot.TeleBot) -> None:
    for el in dict_name_lessons:
        if dict_name_lessons[el][0] == lesson:
            newsletter(user_id=user_id, text=f'⚠ Обновлено Д/З [{dict_name_lessons[el][1]}]', auto=True, bot=bot)
            break
        else:
            continue

    return


def check_for_admin(user_id: int) -> bool:
    for admin_id in config.admin_id:
        if user_id == admin_id:
            log.info(user_id=str(user_id), msg='Admin check: success')
            return True

    return False


def check_user_in_db(message: Any, bot: telebot.TeleBot) -> bool:
    if not db.get_user_authentication(user_id=message.chat.id):
        log.info(user_id=str(message.chat.id), msg='User unauthenticated !')

        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)
        log.info(user_id=str(message.chat.id), msg='Add user . . .')

        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'[ ! ] Ошибка аутентификации !\n[ * ] Данные добавлены !\n\nVersion: {config.version}')

        return False
    else:
        return True

