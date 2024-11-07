import os
import asyncio
import datetime
import multiprocessing
from typing import Any
from sqlite3 import sqlite_version
from base64 import b64decode
from time import strftime, localtime, sleep
from platform import system, release, python_version

import psutil
import telebot
from telebot import types

import db
import config
import loging
import temp_vars
import colors_log
import sgo.NetSchoolAPI as NetSchoolAPI
from utils import rename, send_status_text, newsletter, send_update_dz, check_for_admin, check_user_in_db
from kb import gen_markup_start, markup_dz, markup_dz_update, markup_dz_update_p, markup_update_dz_or_gdz, markup_url, del_schedule_button, markup_del_schedule_warn, markup_admin_panel, markup_off_notifications_warn, markup_chack_mailing, check, back_in_main_menu, gen_profile_markup, markup_NetSchool, gen_announcements
import utils

bot: telebot.TeleBot = telebot.TeleBot(config.BotToken, parse_mode='html')

log = loging.logging(Name='MAIN', Color=colors_log.green)
log_grade = loging.logging(Name='MAIN_G', Color=colors_log.purple)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tmp_vars = temp_vars.tmp_vars

log.info(user_id=None, msg='The bot is running !')


def notification_admin(text: str, reply_markup: telebot.types.InlineKeyboardMarkup | None = None) -> None:
    log.info(user_id=None, msg='Sending notifications to admins . . .')
    for admin_id in config.admin_id:
        try:
            bot.send_message(admin_id, text, reply_markup=reply_markup)
            log.info(user_id=None, msg=f'Send {admin_id} . . .')
        except telebot.apihelper.ApiException:
            log.warn(user_id=str(admin_id), msg=f'Admin {admin_id} blocked or didn\'t start the bot!')


def check_grade(sleep_sec: float = 300) -> None:
    while True:
        # TODO: Проверка на наличие новых оценок
        log_grade.info(user_id=None, msg='Check for new grade')
        sleep(sleep_sec)


def check_client_NetSchoolAPI(user_id: int, msg_id: int) -> None:
    if temp_vars.get_logined_net_school(self=tmp_vars, user_id=user_id) == ValueError:
        bot.edit_message_text(chat_id=user_id, message_id=msg_id, text='Ошибка ! Не найден клиент NetSchoolAPI. Войдите в акаунт заново.',
                              reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                                  types.InlineKeyboardButton(text='🔄 Повторная авторизация', callback_data='netschool'),
                                  back_in_main_menu
                                  ))
    else:
        return


# Command
@bot.message_handler(commands=['start'])
def start(message: Any) -> None:
    log.info(user_id=str(message.chat.id), msg='Received \'/start\'')

    if check_for_admin(user_id=message.chat.id):
        log.info(user_id=str(message.chat.id), msg='Admin pressed \'/start\'')

        send_status_text(user_id=message.chat.id, bot=bot)
        bot.send_message(message.chat.id, f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=gen_markup_start(user_id=message.chat.id))

    else:
        log.info(user_id=str(message.chat.id), msg='User (authenticated) pressed \'/start\'')

        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)

        send_status_text(user_id=message.chat.id, bot=bot)
        bot.send_message(message.chat.id, f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=gen_markup_start(user_id=message.chat.id))


@bot.message_handler(commands=['clear_RKM'])
def clear_RKM(message: Any) -> None:
    bot.send_message(message.chat.id, '[INFO] ReplyKeyboardMarkup deleted.', reply_markup=types.ReplyKeyboardRemove())
    start()


# Main Admin Panel
@bot.message_handler(commands=['AdminPanel_4qB7cY9jZ2gP'])
def AdminPanel_4qB7cY9jZ2gP(message: Any) -> None:
    log.warn(user_id=message.chat.id, msg='Admin logged into the panel . . .')
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
    except Exception:
        bot.send_message(chat_id=message.chat.id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)


# Other
@bot.message_handler(content_types=['photo'])
def photo(message: Any) -> None:
    if check_user_in_db(message, bot=bot) and check_for_admin(user_id=message.chat.id):
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = 'photo.jpg'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        if message.caption != None:
            send_status_text(user_id=message.chat.id, bot=bot)
            bot.send_message(chat_id=message.chat.id, text='👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update_p)

            tmp_vars.input_text = message.caption
        else:
            rename(user_id=message.chat.id, file_name_in='photo.jpg', file_name_out='schedule.jpg')

            bot.send_message(chat_id=message.chat.id, text='⚠ Активирована система уведомлений . . .')
            newsletter(user_id=message.chat.id, text='⚠ Обновлено расписание.', auto=True, bot=bot)


# Inline-button
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: Any) -> Any:
    if call.data == 'pass':
        log.info(user_id=str(call.message.chat.id), msg=f'Call \'[{call.data}]\'')
        return

    elif check_user_in_db(message=call.message, bot=bot):
        log.info(user_id=str(call.message.chat.id), msg=f'Call \'[{call.data}]\'')
        # Main menu
        if call.data == 'dz':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет', reply_markup=markup_dz)
        elif call.data == 'schedule':
            log.info(user_id=str(call.message.chat.id), msg='Received \'/schedule\'')
            try:
                open_photo = open('schedule.jpg', 'rb')
                bot.send_chat_action(call.message.chat.id, action='upload_photo')
                if check_for_admin(user_id=call.message.chat.id):
                    bot.send_photo(call.message.chat.id, photo=open_photo, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(del_schedule_button, back_in_main_menu))
                else:
                    bot.send_photo(call.message.chat.id, photo=open_photo, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
            except FileNotFoundError:
                log.warn(user_id=str(call.message.chat.id), msg='Schedule not found !')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ошибка: файл не найден.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))

                notification_admin(text='Файл расписание не найден.\nПожалуйста добавьте расписание !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
        elif call.data == 'call_schedule':
            log.info(user_id=str(call.message.chat.id), msg='Received \'/call_schedule\'')
            if datetime.datetime.isoweekday(datetime.datetime.now()) < 5 or datetime.datetime.isoweekday(datetime.datetime.now()) > 5:
                call_schedule = '''Урок 1: 8:00   -  8:45\nУрок 2: 8:55   -  9:40\nУрок 3: 10:00 - 10:45\nУрок 4: 11:05 - 11:50\nУрок 5: 12:00 - 12:45\nУрок 6: 12:55 - 13:40\nУрок 7: 13:45 - 14:30\nУрок 8: 14:35 - 15:20'''

                lessons = [
                    {'start_time': 8_00, 'end_time': 8_45},
                    {'start_time': 8_55, 'end_time': 9_40},
                    {'start_time': 10_00, 'end_time': 10_45},
                    {'start_time': 11_05, 'end_time': 11_50},
                    {'start_time': 12_00, 'end_time': 12_45},
                    {'start_time': 12_55, 'end_time': 13_40},
                    {'start_time': 13_45, 'end_time': 14_30},
                    {'start_time': 14_35, 'end_time': 15_20}
                        ]
            elif datetime.datetime.isoweekday(datetime.datetime.now()) == 5:
                call_schedule = '''⚠️ Расписание на пятницу\nУрок 1: 8:00   -  8:45\nУрок 2: 8:55   -  9:35\nУрок 3: 9:55   - 10:35\nУрок 4: 10:55 - 11:35\nУрок 5: 11:45 - 12:20\nУрок 6: 12:30 - 13:10'''

                lessons = [
                    {'start_time': 8_00, 'end_time': 8_45},
                    {'start_time': 8_55, 'end_time': 9_35},
                    {'start_time': 9_55, 'end_time': 10_35},
                    {'start_time': 10_55, 'end_time': 11_35},
                    {'start_time': 11_45, 'end_time': 12_20},
                    {'start_time': 12_30, 'end_time': 13_10}
                ]

            current_time = int(strftime('%H%M', localtime()))

            log.info(user_id=str(call.message.chat.id), msg='The enumeration of all lessons and variables has begun')
            for lesson in lessons:
                start_time = lesson['start_time']
                end_time = lesson['end_time']

                if start_time <= current_time <= end_time:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{call_schedule}\n\nДо конца урока осталось: {divmod(end_time - current_time, 60)[0]} часов и {(end_time - current_time) - (divmod(end_time - current_time, 60)[0] * 60)} минут.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
                    return 0

            if (min(lessons, key=lambda x: abs(x['start_time'] - current_time))['start_time'] / 100 * 60 + min(lessons, key=lambda x: abs(x['start_time'] - current_time))['start_time'] % 100) - (current_time / 100 * 60 + current_time % 100) >= 0:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{call_schedule}\n\nСледующий урок через {divmod((min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] / 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time / 100 * 60 + current_time % 100), 60)[0]} часов {(min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] / 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time / 100 * 60 + current_time % 100) - (divmod((min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] / 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time / 100 * 60 + current_time % 100), 60)[0] * 60)} минут', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{call_schedule}\n\nУроки закончились на сегодня!', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
        elif call.data == 'profile':
            if tmp_vars.on_net_school_list_users != []:
                try:
                    tmp_vars.on_net_school_list_users.remove(call.message.chat.id)
                except ValueError:
                    pass

            try:
                rsn = db.get_send_notifications(user_id=call.message.chat.id)
                net_school = db.get_net_school(user_id=call.message.chat.id)
                isAdmin: bool | str = utils.check_for_admin(user_id=call.message.chat.id)

                if rsn:
                    notifications_status = '✅'
                else:
                    notifications_status = '❌'

                if net_school == None:
                    net_school_status = '❌'
                else:
                    net_school_status = '✅'

                if isAdmin:
                    isAdmin = '✅'
                else:
                    isAdmin = '❌'

                data = db.get_user_id(user_id=call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'ID-TELEGRAM: {call.message.chat.id}\nВаше имя: @{data[2]}\nВаш никнейм: {data[3]}\nУведомления: {notifications_status}\nИнтеграция с СГО: {net_school_status}\nПрава администратора: {isAdmin}', reply_markup=gen_profile_markup(rsn=rsn, net_school=net_school))
            except Exception as Error:
                log.error(user_id=call.message.chat.id, msg=str(Error))
        # Show D/Z
        elif check(input=call.data, pstr_cbd=''):
            if tmp_vars.press_button_notification_admin_list_users != {}:
                try:
                    tmp_vars.logined_net_school_list_users.pop(call.message.chat.id)
                except Exception:
                    pass

            markup_back = types.InlineKeyboardMarkup(row_width=1)
            url = db.get_url(user_id=call.message.chat.id, lesson=call.data)
            photo = db.get_photo(user_id=call.message.chat.id, lesson=call.data)

            notification_admin_b = types.InlineKeyboardButton(text='⚠️ Задание не верное или устаревшее ⚠️', callback_data=f'{call.data}_notification_admin')
            del_dz = types.InlineKeyboardButton(text='❌ Удалить Д/З ❌', callback_data=f'{call.data}_del_dz_warn')
            back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back_dz')

            # URL
            if url != 'None':
                url = types.InlineKeyboardButton(text='ГДЗ', url=url)

                if check_for_admin(user_id=call.message.chat.id):
                    markup_back.add(url, del_dz, back, back_in_main_menu)
                else:
                    markup_back.add(url, notification_admin, back, back_in_main_menu)
            else:
                if check_for_admin(user_id=call.message.chat.id):
                    markup_back.add(del_dz, back, back_in_main_menu)
                else:
                    markup_back.add(notification_admin_b, back, back_in_main_menu)
            # Photo
            if photo != 'None':
                bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
                bot.send_chat_action(call.message.chat.id, action='upload_photo')
                bot.send_photo(call.message.chat.id, photo=open(file=photo, mode='rb'), caption=str(db.get_dz(user_id=call.message.chat.id, lesson=call.data)), reply_markup=markup_back)
            # Default
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(db.get_dz(user_id=call.message.chat.id, lesson=call.data)), reply_markup=markup_back)
        # WARN Del D/Z
        elif check(input=call.data, pstr_cbd='_del_dz_warn'):
            markup_del_dz_warn = types.InlineKeyboardMarkup(row_width=1)
            yes = types.InlineKeyboardButton(text='✅ Да ✅', callback_data=call.data.replace('_warn', ''))
            no = types.InlineKeyboardButton(text='❌ Нет ❌', callback_data=call.data.replace('_del_dz_warn', ''))
            markup_del_dz_warn.add(yes, no)
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"⚠ Вы уверены ?\n\nД/З: {db.get_dz(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz_warn', ''))}", reply_markup=markup_del_dz_warn)
            except Exception:
                log.info(user_id=str(call.message.chat.id), msg='Error in edit_message_text')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=f"⚠ Вы уверены ?\n\nД/З: {db.get_dz(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz_warn', ''))} + Photo", reply_markup=markup_del_dz_warn)
        # Del D/Z
        elif check(input=call.data, pstr_cbd='_del_dz'):
            send_status_text(user_id=call.message.chat.id, bot=bot)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется удаление, пожалуйста, подождите . . .')
            db.set_dz(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz', ''), dz='Не добавлено домашнее задание =(')
            db.set_photo(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz', ''), path='None')
            try:
                os.remove('photo/' + call.data.replace('_del_dz', '') + '.jpg')
            except FileNotFoundError:
                pass
            db.set_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace('_del_dz', ''))
            log.warn(user_id=str(call.message.chat.id), msg=f"Admin deleted dz \'{call.data.replace('_del_dz', '')}\'")
            send_status_text(user_id=call.message.chat.id, bot=bot)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data=call.data.replace('_del_dz', '')), back_in_main_menu))

        # WARN Del schedule
        elif call.data == 'schedule_del_warn':
            bot.send_message(chat_id=call.message.chat.id, text='⚠ Вы уверены ?\n\nSchedule', reply_markup=markup_del_schedule_warn)
        # Del schedule
        elif call.data == 'schedule_del':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется удаление, пожалуйста, подождите . . .')
            try:
                os.remove('schedule.jpg')
            except FileNotFoundError:
                pass
            log.warn(user_id=str(call.message.chat.id), msg='Admin deleted schedule')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='schedule'), back_in_main_menu))
        # No del schedule
        elif call.data == 'schedule_del_no':
            bot.delete_message(call.message.chat.id, message_id=call.message.message_id)

        # Notification admin
        elif check(input=call.data, pstr_cbd='_notification_admin'):

            tmp_vars.press_button_notification_admin_list_users.update({(call.message.chat.id, call.data.replace('_notification_admin', ''))})
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠️ Введите комментарий к запросу в нём можно указать на ошибку или предложить правильное Д/З',
                                  reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data=call.data.replace('_notification_admin', '')), back_in_main_menu))
        # Back
        elif call.data == 'back_dz':
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет', reply_markup=markup_dz)
            except telebot.apihelper.ApiException as Error:
                if Error.result.status_code == 400:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_status_text(user_id=call.message.chat.id, bot=bot)
                    bot.send_message(call.message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)
        elif call.data == 'back_in_main_menu':
            if tmp_vars.on_net_school_list_users != []:
                try:
                    tmp_vars.on_net_school_list_users.remove(call.message.chat.id)
                except ValueError:
                    pass
            if tmp_vars.login_net_school_list_users != []:
                try:
                    tmp_vars.login_net_school_list_users.remove(call.message.chat.id)
                except ValueError:
                    pass
            if tmp_vars.logined_net_school_list_users != {}:
                try:
                    tmp_vars.logined_net_school_list_users.pop(call.message.chat.id)
                except Exception:
                    pass
            if tmp_vars.press_button_notification_admin_list_users != {}:
                try:
                    tmp_vars.logined_net_school_list_users.pop(call.message.chat.id)
                except Exception:
                    pass
            if tmp_vars.input_text != r'None':
                tmp_vars.input_text = r'None'
            if tmp_vars.input_text_mailing != None:
                tmp_vars.input_text_mailing = None

            cfa = check_for_admin(user_id=call.message.chat.id)
            try:
                if cfa:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=gen_markup_start(user_id=call.message.chat.id))
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=gen_markup_start(user_id=call.message.chat.id))
            except Exception:
                if cfa:
                    bot.send_message(chat_id=call.message.chat.id, text=f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=gen_markup_start(user_id=call.message.chat.id))
                else:
                    bot.send_message(chat_id=call.message.chat.id, text=f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=gen_markup_start(user_id=call.message.chat.id))

        # § (Paragraph)
        elif call.data == 'paragraph':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=r'§')

        # Replace D/Z
        elif check(input=call.data, pstr_cbd='_update'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется замена, пожалуйста, подождите . . .')

            db.set_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update', ''), dz=tmp_vars.input_text)
            db.set_photo(user_id=call.message.chat.id, lesson=call.data.replace('_update', ''), path='None')

            try:
                os.remove('photo/' + call.data.replace('_update', '') + '.jpg')
            except FileNotFoundError:
                pass

            db.set_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace('_update', ''))

            log.info(user_id=str(call.message.chat.id), msg='Successfully !')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠ Активирована система уведомлений . . .')
            send_update_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update', ''), bot=bot)
        # Replace D/Z + photo
        elif check(input=call.data, pstr_cbd='_update_p'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется замена, пожалуйста, подождите . . .')

            rename(user_id=call.message.chat.id, file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace('_update_p', '') + '.jpg')

            db.set_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update_p', ''), dz=tmp_vars.input_text)
            db.set_photo(user_id=call.message.chat.id, lesson=call.data.replace('_update_p', ''), path='photo/' + call.data.replace('_update_p', '') + '.jpg')
            db.set_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace('_update_p', ''))

            log.info(user_id=str(call.message.chat.id), msg='Successfully !')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠ Активирована система уведомлений . . .')
            send_update_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update_p', ''), bot=bot)
        # Replace URL
        elif check(input=call.data, pstr_cbd='_url'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется замена, пожалуйста, подождите . . .')

            db.set_url(user_id=call.message.chat.id, url=tmp_vars.input_text, lesson=call.data.replace('_url', ''))

            log.info(user_id=str(call.message.chat.id), msg='Successfully !')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))

        # Notifications
        elif call.data == 'off_notifications_warn':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы уверены ?\n\n*Если вы отключите уведомления вы не будете получать сообщения об обновлении домашнего задания и расписания. Сюда НЕ входит рассылка от администраторов бота.', reply_markup=markup_off_notifications_warn)
        elif call.data == 'off_notifications':
            try:
                db.set_send_notifications(user_id=call.message.chat.id, send_notifications=False)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно! Вы больше не будете получать уведомления.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
            except Exception as Error:
                log.warn(user_id=str(call.message.chat.id), msg=f'Error: {Error}')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'❌ Произошла ошибка при попытке обращения к базе данных. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
        elif call.data == 'on_notifications':
            try:
                db.set_send_notifications(user_id=call.message.chat.id, send_notifications=True)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно! Вы будете получать уведомления.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
            except Exception as Error:
                log.warn(user_id=str(call.message.chat.id), msg=f'Error: {Error}')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'❌ Произошла ошибка при попытке обращения к базе данных. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))

#########################################

        # On NetSchool
        elif call.data == 'on_net_school':
            tmp_vars.on_net_school_list_users.append(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите данные в таком формате:\nлогин<b>[пробел]</b>пароль<b>[пробел]</b>ключ шифрования\nНапример:\n<b>ПетровА0 12345678 qwerty</b>', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))

        # Login
        elif call.data == 'netschool':
            if temp_vars.get_logined_net_school(self=tmp_vars, user_id=call.message.chat.id) == ValueError:
                tmp_vars.login_net_school_list_users.append(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите ключ шифрования', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='NetSchool', reply_markup=markup_NetSchool)

        # diary
        elif call.data == 'diary':
            check_client_NetSchoolAPI(user_id=call.message.chat.id, msg_id=call.message.message_id)

            data_diary = loop.run_until_complete(NetSchoolAPI.diary(NSAPI=temp_vars.get_logined_net_school(self=tmp_vars, user_id=call.message.chat.id)))

            if type(data_diary) is type(str):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=data_diary, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='netschool'), back_in_main_menu))
                return

            log.warn(user_id=call.message.chat.id, msg=str(data_diary))

        # Overdues
        elif call.data == 'overdue':
            check_client_NetSchoolAPI(user_id=call.message.chat.id, msg_id=call.message.message_id)

            data_overdue = loop.run_until_complete(NetSchoolAPI.overdue(NSAPI=temp_vars.get_logined_net_school(self=tmp_vars, user_id=call.message.chat.id)))
            log.warn(user_id=call.message.chat.id, msg=str(data_overdue))

        # Announcements
        elif call.data == 'announcements':
            check_client_NetSchoolAPI(user_id=call.message.chat.id, msg_id=call.message.message_id)

            data_announcements = loop.run_until_complete(NetSchoolAPI.announcements(NSAPI=temp_vars.get_logined_net_school(self=tmp_vars, user_id=call.message.chat.id)))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='NetSchool/Объявления', reply_markup=gen_announcements(an=data_announcements))
        elif call.data.startswith('announcements:'):
            check_client_NetSchoolAPI(user_id=call.message.chat.id, msg_id=call.message.message_id)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Обработка', reply_markup=types.InlineKeyboardMarkup(row_width=1))

            name = str(b64decode(str(call.data).split(':')[-1]).decode('utf-8'))
            announcement: NetSchoolAPI.types_NSAPI.schemas.Announcement | None = None
            data_announcements = loop.run_until_complete(NetSchoolAPI.announcements(NSAPI=temp_vars.get_logined_net_school(self=tmp_vars, user_id=call.message.chat.id)))
            for announcements in data_announcements:
                if announcements.name[0:8] == name:
                    announcement = announcements
                    break
                else:
                    continue

            if announcement == None:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='❌ Incorrect call', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='announcements'), back_in_main_menu))
                return

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Имя: <b>{announcement.name}</b>\n\nАвтор: <code>{announcement.author.full_name}</code>\n\nТекст: <b>{utils.convert_html_to_text(announcement.content)}</b>', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='announcements'), back_in_main_menu))  # type: ignore[union-attr]

        # Info school
        elif call.data == 'school':
            check_client_NetSchoolAPI(user_id=call.message.chat.id, msg_id=call.message.message_id)

            data_school = loop.run_until_complete(NetSchoolAPI.info_school(NSAPI=temp_vars.get_logined_net_school(self=tmp_vars, user_id=call.message.chat.id)))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Имя: <code>{data_school.name}</code>\n\nАдрес: <code>{data_school.address}</code>\nE-mail: <code>{data_school.email}</code>\nСайт: <code>{data_school.site}</code>\nТелефон: <code>{data_school.phone}</code>\n\nДиректор: {data_school.director}\nAHC: {data_school.AHC}\nUVR: {data_school.UVR}',
                                  reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='netschool'), back_in_main_menu))


#########################################

        # For admins
        if check_for_admin(user_id=call.message.chat.id):
            # Update dz or gdz
            # DZ
            if call.data == 'update_dz':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update)
            # GDZ
            elif call.data == 'update_gdz':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет по которому хотите заменить ГДЗ', reply_markup=markup_url)

            # Admin panel
            elif call.data == 'admin_panel':
                log.warn(user_id=call.message.chat.id, msg='Admin logged into the panel . . .')
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
                except Exception:
                    bot.send_message(chat_id=call.message.chat.id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
            # Newsletter
            elif call.data == 'newsletter':
                # Запрашиваем ввод у пользователя
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите что-нибудь:')
                tmp_vars.newsletter = True
            elif call.data == 'chack_mailing_yes':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Рассылка началась!')

                newsletter(user_id=call.message.chat.id, text=str(tmp_vars.input_text_mailing), auto=False, bot=bot)
            elif call.data == 'chack_mailing_no':
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
                except Exception:
                    bot.send_message(chat_id=call.message.chat.id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
            # Server status
            elif call.data == 'status_server':
                log.info(user_id=str(call.message.chat.id), msg='Аdmin requested a server status report, generation . . .')

                log.info(user_id=str(call.message.chat.id), msg='Generating information about: SystemName')
                SystemName = str(system())

                log.info(user_id=str(call.message.chat.id), msg='Generating information about: SystemRelease')
                SystemRelease = str(release())

                log.info(user_id=str(call.message.chat.id), msg='Generating information about: PythonVersion')
                PythonVersion = str(python_version())

                log.info(user_id=str(call.message.chat.id), msg='Generating information about: SQLite3Version')
                SQLite3Version = str(sqlite_version)

                # Загруженость
                # CPU
                log.info(user_id=str(call.message.chat.id), msg='Generating information about: CPU')
                cpu = psutil.cpu_percent(interval=1)

                # Memory
                log.info(user_id=str(call.message.chat.id), msg='Generating information about: Memory, Memory_Swap')
                Memory = psutil.virtual_memory()
                Memory_Swap = psutil.swap_memory()

                # Disks
                log.info(user_id=str(call.message.chat.id), msg='Generating information about: Disks')
                Disks = psutil.disk_usage('/')

                # Network
                log.info(user_id=str(call.message.chat.id), msg='Generating information about: Network')
                all_interf = psutil.net_if_addrs()
                Network: str = '\n'

                for interf in all_interf:
                    Network = f'{Network}- {interf}: {all_interf[interf][0][1]}\n'

                log.info(user_id=str(call.message.chat.id), msg='Generating a report based on the data received . . .')
                report = f'OS: {SystemName} {SystemRelease}\nPython: {PythonVersion}\nSQLite3: {SQLite3Version}\n\nЗагруженость:\n\nCPU: {cpu}%\nMemory: {Memory.percent}%\nMemory Swap: {Memory_Swap.percent}%\nDisks: {Disks.percent}%\nNetwork: {Network}'
                log.info(user_id=str(call.message.chat.id), msg='Successfully !')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=report, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='chack_mailing_no'), back_in_main_menu))

                log.info(user_id=str(call.message.chat.id), msg='Report Sent !')


# Text
@bot.message_handler(content_types=['text'])
def logic(message: Any) -> Any:
    if check_user_in_db(message, bot=bot):
        log.info(user_id=str(message.chat.id), msg=f'Received \'{message.text}\'')
        # NetSchool
        if [message.chat.id == user_id for user_id in tmp_vars.on_net_school_list_users]:
            tmp_vars.on_net_school_list_users.remove(message.chat.id)
            try:
                login = message.text.split(' ')[0]
                password = message.text.split(' ')[1]
                key = message.text.split(' ')[2]
            except IndexError:
                bot.send_message(message.chat.id, 'Неверный формат!', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='on_net_school'), back_in_main_menu))
                return

            msg_id = bot.send_message(message.chat.id, '⚠️ Проверка возможности входа . . .').message_id

            try:
                client_NetSchoolAPI = loop.run_until_complete(NetSchoolAPI.create_client(API=config.API_NetSchool))
                loop.run_until_complete(NetSchoolAPI.login(NSAPI=client_NetSchoolAPI, login=login, password=password, school=config.School_NetSchool))
                loop.run_until_complete(NetSchoolAPI.logout(NSAPI=client_NetSchoolAPI))

                bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='✅ Успешно\n\nИнтеграция с СГО подключена !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))

            except ValueError:
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='❌ Вход не удался', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='on_net_school'), back_in_main_menu))
                return

            except Exception as Error:
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=f'❌ Произошла ошибка при попытке обращения к NetSchoolAPI.login. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
                return

            try:
                db.set_net_school(user_id=message.chat.id, login=login, password=password, key=key)
                return
            except Exception as Error:
                bot.send_message(chat_id=message.chat.id, text=f'❌ Произошла ошибка при попытке обращения к базе данных. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
                return
        elif [message.chat.id == user_id for user_id in tmp_vars.login_net_school_list_users]:
            try:
                msg_id = bot.send_message(message.chat.id, '⚙️ Инициализация входа . . .').message_id

                key = message.text
                ns_data = db.get_net_school(user_id=message.chat.id)

                if key != ns_data['key']:  # type: ignore[index]
                    bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='⚙️ Вход . . .')
                    bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='❌ Вход не удался', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
                    return

                client_NetSchoolAPI = loop.run_until_complete(NetSchoolAPI.create_client(API=config.API_NetSchool, requests_timeout=60))

                bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='⚙️ Вход . . .')

                loop.run_until_complete(
                    NetSchoolAPI.login(
                        NSAPI=client_NetSchoolAPI,
                        login=ns_data['login'],  # type: ignore[index]
                        password=ns_data['password'],  # type: ignore[index]
                        school=config.School_NetSchool
                        ))

                tmp_vars.logined_net_school_list_users.update({(message.chat.id, client_NetSchoolAPI)})
                temp_vars.get_logined_net_school(self=tmp_vars, user_id=message.chat.id)

                bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='NetSchool', reply_markup=markup_NetSchool)
            except Exception as Error:
                bot.send_message(chat_id=message.chat.id, text=f'❌ Произошла ошибка. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(back_in_main_menu)))

        # Notifications admin
        elif False:
            log.info(user_id=str(message.chat.id), msg=f'User: {message.chat.id} requested a D/Z update')

            if str(message.text)[0] == '/':
                send_status_text(user_id=message.chat.id, bot=bot)
                bot.send_message(message.chat.id, '⚠️ Отправка прервана.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data=tmp_vars.press_button_notification_admin_list_users[message.chat.id]), back_in_main_menu))
            else:
                notification_admin_ = multiprocessing.Process(target=notification_admin, args=(f'⚠️ Пользователь: {message.chat.id} уведомил вас в неактуальности Д/З по q\n\nКомментарий: {message.text}', None))
                notification_admin_.start()

                bot.send_message(message.chat.id, '✅ Отчёт успешно отправлен. Извините за неудобства.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data=str(tmp_vars.press_button_notification_admin_list_users[message.chat.id])), back_in_main_menu))

                notification_admin_.join()

        # Main Admin Panel
        elif check_for_admin(user_id=message.chat.id) and tmp_vars.newsletter:
            tmp_vars.input_text_mailing = message.text
            tmp_vars.newsletter = False

            send_status_text(user_id=message.chat.id, bot=bot)
            bot.send_message(message.chat.id, f'<u><b>‼️ВЫ ТОЧНО ХОТИТЕ ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ ПОЛЬЗОВАТЕЛЯМ⁉️</b></u>\nТЕКСТ СООБЩЕНИЯ:\n{tmp_vars.input_text_mailing}', parse_mode='html', reply_markup=markup_chack_mailing)

        # Panel replace
        elif check_for_admin(user_id=message.chat.id):
            send_status_text(user_id=message.chat.id, bot=bot)
            bot.send_message(message.chat.id, 'Где нужно поставить этот текст ?', reply_markup=markup_update_dz_or_gdz)

            tmp_vars.input_text = message.text
        else:
            log.info(user_id=str(message.chat.id), msg=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')

            send_status_text(user_id=message.chat.id, bot=bot)
            bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))


if __name__ == 'main':
    notification_admin_ = multiprocessing.Process(target=notification_admin, args=(f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}', None))
    chk_grade = multiprocessing.Process(target=check_grade)

    notification_admin_.start()
    # chk_grade.start()
    bot.infinity_polling(timeout=60, long_polling_timeout=60, logger_level=0, interval=0)

    # chk_grade.kill()
    notification_admin_.kill()
else:
    log.cerror(user_id=None, msg=f"__name__ == \'main\': {__name__ == 'main'}")
