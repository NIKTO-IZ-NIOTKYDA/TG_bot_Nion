import os
import datetime
from typing import Any
from sqlite3 import sqlite_version
from time import sleep, strftime, localtime
from platform import system, release, python_version

import psutil
import telebot
from telebot import types

import db
import config
import loging
import colors_log
from kb import markup_start, markup_dz, markup_dz_update, markup_dz_update_p, markup_update_dz_or_gdz, markup_url, del_schedule_button, markup_del_schedule_warn, markup_admin_panel, markup_off_notifications_warn, markup_chack_mailing, check, back_in_main_menu, dict_name_lessons, gen_notifications_markup

bot: telebot.TeleBot = telebot.TeleBot(config.BotToken)

log = loging.logging(Name='MAIN', Color=colors_log.green)
log.info(user_id=None, do='The bot is running !')


# main fn
def rename(user_id: int, file_name_in: str, file_name_out: str) -> None:
    log.info(user_id=str(user_id), do=f'Rename {file_name_in} -> {file_name_out}')
    try:
        os.system(f'mv {file_name_in} {file_name_out}')
        log.info(user_id=str(user_id), do='Successfully !')
    except Exception as Error:
        log.error(user_id=str(user_id), do=str(Error))


def send_status_text(user_id: int) -> None:
    if config.debug:
        log.info(user_id=str(user_id), do='Send status . . .')
    bot.send_chat_action(user_id, action='typing')


def newsletter(user_id: int, text: str, auto: bool) -> None:
    log.warn(user_id=str(user_id), do='Start of the mailing')

    all_user_id = db.return_all_user_id(user_id, auto=auto)

    if all_user_id != None:
        timer: int = 0

        for user_id in all_user_id:  # type: ignore[union-attr]
            if timer < 29:
                try:
                    bot.send_message(chat_id=user_id, text=text)
                    log.info(user_id=str(user_id), do=f'Sent: {user_id}')

                    timer += 1
                    continue
                except telebot.apihelper.ApiException as Error:
                    if Error.result.status_code == 403 or Error.result.status_code == 400:
                        log.warn(user_id=str(user_id), do=f'User {user_id} has blocked the bot!')
                        # db.remove_user(user_id=str(user_id))

                        timer += 1
                        continue
                except Exception as Error:
                    log.error(user_id=str(user_id), do=str(Error))

                    timer += 1
                    continue
            else:
                sleep(1.15)
                timer = 0

        log.info(user_id=str(user_id), do='Mailing is over')
        bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
        return
    else:
        log.info(user_id=str(user_id), do='Mailing is over')
        bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))
        return


def send_update_dz(user_id: int, lesson: str) -> None:
    for el in dict_name_lessons:
        newsletter(user_id=user_id, text=f'⚠ Обновлено Д/З [{dict_name_lessons[el][1]}]', auto=True)
        return


def check_for_admin(user_id: int) -> bool:
    for admin_id in config.admin_id:
        if user_id == admin_id:
            log.info(user_id=str(user_id), do='Admin check: success')
            return True

    return False


def check_user_in_db(message: Any) -> bool:
    if not db.return_user_authentication(user_id=message.chat.id):
        log.info(user_id=str(message.chat.id), do='User unauthenticated !')

        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)
        log.info(user_id=str(message.chat.id), do='Add user . . .')

        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'[ ! ] Ошибка аутентификации !\n[ * ] Данные добавлены !\n\nVersion: {config.version}')

        return False
    else:
        return True


def notification_admin(text: str) -> None:
    log.info(user_id='none', do='Sending notifications to admins . . .')
    for admin_id in config.admin_id:
        try:
            bot.send_message(admin_id, text)
        except telebot.apihelper.ApiException:
            log.warn(user_id=str(admin_id), do=f'Admin {admin_id} blocked or didn\'t start the bot!')


# Command
@bot.message_handler(commands=['start'])
def start(message: Any) -> None:
    log.info(user_id=str(message.chat.id), do='Received \'/start\'')

    if check_for_admin(user_id=message.chat.id):
        log.info(user_id=str(message.chat.id), do='Admin pressed \'/start\'')

        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=markup_start)

    else:
        log.info(user_id=str(message.chat.id), do='User (authenticated) pressed \'/start\'')

        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)

        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=markup_start)


@bot.message_handler(commands=['clear_RKM'])
def clear_RKM(message: Any) -> None:
    bot.send_message(message.chat.id, '[INFO] ReplyKeyboardMarkup deleted.', reply_markup=types.ReplyKeyboardRemove())
    start()


# Main Admin Panel
@bot.message_handler(commands=['AdminPanel_4qB7cY9jZ2gP'])
def AdminPanel_4qB7cY9jZ2gP(message: Any) -> None:
    log.warn(user_id=message.chat.id, do='Admin logged into the panel . . .')
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
    except Exception:
        bot.send_message(chat_id=message.chat.id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)


# Other
@bot.message_handler(content_types=['photo'])
def photo(message: Any) -> None:
    if check_user_in_db(message) and check_for_admin(user_id=message.chat.id):
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = 'photo.jpg'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        if message.caption != None:
            send_status_text(user_id=message.chat.id)
            bot.send_message(chat_id=message.chat.id, text='👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update_p)

            config.input_text = message.caption
        else:
            rename(user_id=message.chat.id, file_name_in='photo.jpg', file_name_out='schedule.jpg')

            bot.send_message(chat_id=message.chat.id, text='⚠ Активирована система уведомлений . . .')

            newsletter(user_id=message.chat.id, text='⚠ Обновлено расписание.', auto=True)


# Inline-button
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: Any) -> Any:
    if check_user_in_db(message=call.message):
        log.info(user_id=str(call.message.chat.id), do=f'Call \'[{call.data}]\'')
        # Main menu
        if call.data == 'dz':
            if check_user_in_db(call.message):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет', reply_markup=markup_dz)
        elif call.data == 'schedule':
            log.info(user_id=str(call.message.chat.id), do='Received \'/schedule\'')
            try:
                open_photo = open('schedule.jpg', 'rb')
                bot.send_chat_action(call.message.chat.id, action='upload_photo')
                if check_for_admin(user_id=call.message.chat.id):
                    bot.send_photo(call.message.chat.id, photo=open_photo, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(del_schedule_button, back_in_main_menu))
                else:
                    bot.send_photo(call.message.chat.id, photo=open_photo, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(del_schedule_button, back_in_main_menu))
            except FileNotFoundError:
                log.warn(user_id=str(call.message.chat.id), do='Schedule not found !')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ошибка: файл не найден.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))

                notification_admin(text='Файл расписание не найден.\nПожалуйста добавьте расписание !')
        elif call.data == 'call_schedule':
            if check_user_in_db(call.message):
                log.info(user_id=str(call.message.chat.id), do='Received \'/call_schedule\'')

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

                log.info(user_id=str(call.message.chat.id), do='The enumeration of all lessons and variables has begun')
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
            rsn = db.return_send_notifications(user_id=call.message.chat.id)

            if rsn:
                notifications_status = '✅'
            else:
                notifications_status = '❌'

            data = db.return_user_id(user_id=call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'ID-TELEGRAM: {call.message.chat.id}\nВаше имя: @{data[2]}\nВаш никнейм: {data[3]}\nУведомления: {notifications_status}', reply_markup=gen_notifications_markup(rsn=rsn))
        # Show D/Z
        elif check(input=call.data, pstr_cbd=''):
            markup_back = types.InlineKeyboardMarkup(row_width=1)
            url = db.return_url(user_id=call.message.chat.id, lesson=call.data)[0]
            photo = db.return_photo(user_id=call.message.chat.id, lesson=call.data)[0]

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
                bot.send_photo(call.message.chat.id, photo=open(file=photo, mode='rb'), caption=str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]), reply_markup=markup_back)
            # Default
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]), reply_markup=markup_back)
        # WARN Del D/Z
        elif check(input=call.data, pstr_cbd='_del_dz_warn'):
            markup_del_dz_warn = types.InlineKeyboardMarkup(row_width=1)
            yes = types.InlineKeyboardButton(text='✅ Да ✅', callback_data=call.data.replace('_warn', ''))
            no = types.InlineKeyboardButton(text='❌ Нет ❌', callback_data=call.data.replace('_del_dz_warn', ''))
            markup_del_dz_warn.add(yes, no)
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"⚠ Вы уверены ?\n\nД/З: {db.return_dz(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz_warn', ''))[0]}", reply_markup=markup_del_dz_warn)
            except Exception:
                log.info(user_id=str(call.message.chat.id), do='Error in edit_message_text')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=f"⚠ Вы уверены ?\n\nД/З: {db.return_dz(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz_warn', ''))[0]} + Photo", reply_markup=markup_del_dz_warn)
        # Del D/Z
        elif check(input=call.data, pstr_cbd='_del_dz'):
            send_status_text(user_id=call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется удаление, пожалуйста, подождите . . .')
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz', ''), dz='Не добавлено домашнее задание =(')
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace('_del_dz', ''), path='None')
            try:
                os.remove('photo/' + call.data.replace('_del_dz', '') + '.jpg')
            except FileNotFoundError:
                pass
            db.replace_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace('_del_dz', ''))
            log.warn(user_id=str(call.message.chat.id), do=f"Admin deleted dz \'{call.data.replace('_del_dz', '')}\'")
            send_status_text(user_id=call.message.chat.id)
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
            log.warn(user_id=str(call.message.chat.id), do='Admin deleted schedule')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='schedule'), back_in_main_menu))
        # No del schedule
        elif call.data == 'schedule_del_no':
            bot.delete_message(call.message.chat.id, message_id=call.message.message_id)

        # Notification admin
        elif check(input=call.data, pstr_cbd='_notification_admin'):
            log.info(user_id=str(call.message.chat.id), do=f'User: {call.message.chat.id} requested a D/Z update')
            less = call.data.replace('_notification_admin', '')

            def enter_message(call: Any) -> None:
                send_status_text(user_id=call.message.chat.id)
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠️ Введите комментарий к запросу в нём можно указать на ошибку или предложить правильное Д/З', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(msg, start_mailing_admin)

            def start_mailing_admin(call: Any) -> None:
                if call.text[0] == '/':
                    send_status_text(user_id=call.chat.id)
                    bot.send_message(call.message.chat.id, '⚠️ Отправка прервана вы перенаправлены в главное меню.', reply_markup=markup_start)
                else:
                    notification_admin(f'⚠️ Пользователь: {call.chat.id} уведомил вас в неактуальности Д/З по {less}\n\nКомментарий: {call.text}')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Отчёт успешно отправлен. Извините за неудобства.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data=less), back_in_main_menu))

            enter_message(call)

        # Back
        elif call.data == 'back_dz':
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет', reply_markup=markup_dz)
            except telebot.apihelper.ApiException as Error:
                if Error.result.status_code == 400:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_status_text(user_id=call.message.chat.id)
                    bot.send_message(call.message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)
        elif call.data == 'back_in_main_menu':
            try:
                if check_for_admin(user_id=call.message.chat.id):
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=markup_start)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=markup_start)
            except Exception:
                if check_for_admin(user_id=call.message.chat.id):
                    bot.send_message(chat_id=call.message.chat.id, text=f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=markup_start)
                else:
                    bot.send_message(chat_id=call.message.chat.id, text=f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=markup_start)

        # § (Paragraph)
        elif call.data == 'paragraph':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=r'§')

        # Replace D/Z
        elif check(input=call.data, pstr_cbd='_update'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется замена, пожалуйста, подождите . . .')

            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update', ''), dz=config.input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace('_update', ''), path='None')

            try:
                os.remove('photo/' + call.data.replace('_update', '') + '.jpg')
            except FileNotFoundError:
                pass

            db.replace_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace('_update', ''))

            log.info(user_id=str(call.message.chat.id), do='Successfully !')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠ Активирована система уведомлений . . .')
            send_update_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update', ''))
        # Replace D/Z + photo
        elif check(input=call.data, pstr_cbd='_update_p'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется замена, пожалуйста, подождите . . .')

            rename(user_id=call.message.chat.id, file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace('_update_p', '') + '.jpg')

            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update_p', ''), dz=config.input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace('_update_p', ''), path='photo/' + call.data.replace('_update_p', '') + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace('_update_p', ''))

            log.info(user_id=str(call.message.chat.id), do='Successfully !')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠ Активирована система уведомлений . . .')
            send_update_dz(user_id=call.message.chat.id, lesson=call.data.replace('_update_p', ''))
        # Replace URL
        elif check(input=call.data, pstr_cbd='_url'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚙️ Выполняется замена, пожалуйста, подождите . . .')

            db.replace_url(user_id=call.message.chat.id, url=config.input_text, lesson=call.data.replace('_url', ''))

            log.info(user_id=str(call.message.chat.id), do='Successfully !')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно !', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))

        # Notifications
        elif call.data == 'off_notifications_warn':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы уверены ?\n\n*Если вы отключите уведомления вы не будете получать сообщения об обновлении домашнего задания и расписания. Сюда НЕ входит рассылка от администраторов бота.', reply_markup=markup_off_notifications_warn)
        elif call.data == 'off_notifications':
            try:
                db.replace_send_notifications(user_id=call.message.chat.id, send_notifications=False)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно! Вы больше не будете получать уведомления.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
            except Exception as Error:
                log.warn(user_id=str(call.message.chat.id), do=f'Error: {Error}')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'❌ Произошла ошибка при попытке обращения к базе данных. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
        elif call.data == 'on_notifications':
            try:
                db.replace_send_notifications(user_id=call.message.chat.id, send_notifications=True)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Успешно! Вы будете получать уведомления.', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))
            except Exception as Error:
                log.warn(user_id=str(call.message.chat.id), do=f'Error: {Error}')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'❌ Произошла ошибка при попытке обращения к базе данных. Пожалуйста, отправте данный отчёт разработчику бота [@{config.main_admin_url}]: {Error}', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='profile'), back_in_main_menu))

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
            # Newsletter
            elif call.data == 'newsletter':
                # Запрашиваем ввод у пользователя
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите что-нибудь:')
                config.newsletter = True
            elif call.data == 'chack_mailing_yes':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Рассылка началась!')

                newsletter(user_id=call.message.chat.id, text=str(config.input_text_mailing), auto=False)
            elif call.data == 'chack_mailing_no':
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
                except Exception:
                    bot.send_message(chat_id=call.message.chat.id, text='🛠Вы в админ-панели!\nБудте осторожны‼️', reply_markup=markup_admin_panel)
            # Server status
            elif call.data == 'status_server':
                log.info(user_id=str(call.message.chat.id), do='Аdmin requested a server status report, generation . . .')

                log.info(user_id=str(call.message.chat.id), do='Generating information about: SystemName')
                SystemName = str(system())

                log.info(user_id=str(call.message.chat.id), do='Generating information about: SystemRelease')
                SystemRelease = str(release())

                log.info(user_id=str(call.message.chat.id), do='Generating information about: PythonVersion')
                PythonVersion = str(python_version())

                log.info(user_id=str(call.message.chat.id), do='Generating information about: SQLite3Version')
                SQLite3Version = str(sqlite_version)

                # Загруженость
                # CPU
                log.info(user_id=str(call.message.chat.id), do='Generating information about: CPUs, CPU_stats')
                cpu = psutil.cpu_times()
                cpu_stats = psutil.cpu_stats()

                # Memory
                log.info(user_id=str(call.message.chat.id), do='Generating information about: Memory_Virtual, Memory_Swap')
                Memory_Virtual = psutil.virtual_memory()
                Memory_Swap = psutil.swap_memory()

                # Disks
                log.info(user_id=str(call.message.chat.id), do='Generating information about: Disks')
                Disks = psutil.disk_io_counters()

                # Network
                log.info(user_id=str(call.message.chat.id), do='Generating information about: Network')
                Network = psutil.net_if_addrs()

                log.info(user_id=str(call.message.chat.id), do='Generating a report based on the data received . . .')
                info = f'OS: {SystemName} {SystemRelease}\nPython: {PythonVersion} Version\nSQLite3: {SQLite3Version} Version\n\nЗагруженость:\n#~CPU~#\nCPU: {cpu}\nCPU Stats: {cpu_stats}\n#~MEMORY~#\nMemory Virtual: = {Memory_Virtual}\nMemory Swap: = {Memory_Swap}\n#~DISKS~#\nDisks: {Disks}\n#~NETWORK~#\nNetwork: = {Network}'
                log.info(user_id=str(call.message.chat.id), do='Successfully !')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='⬅️  Назад', callback_data='chack_mailing_no'), back_in_main_menu))

                log.info(user_id=str(call.message.chat.id), do='Report Sent !')


# Text
@bot.message_handler(content_types=['text'])
def logic(message: Any) -> Any:
    if check_user_in_db(message):
        log.info(user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
        # Main Admin Panel
        if check_for_admin(user_id=message.chat.id) and config.newsletter:
            config.input_text_mailing = message.text
            config.newsletter = False

            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, f'<u><b>‼️ВЫ ТОЧНО ХОТИТЕ ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ ПОЛЬЗОВАТЕЛЯМ⁉️</b></u>\nТЕКСТ СООБЩЕНИЯ:\n{config.input_text_mailing}', parse_mode='html', reply_markup=markup_chack_mailing)

        # Panel replace
        elif check_for_admin(user_id=message.chat.id):
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, 'Где нужно поставить этот текст ?', reply_markup=markup_update_dz_or_gdz)

            config.input_text = message.text
        else:
            log.info(user_id=str(message.chat.id), do=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')

            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(back_in_main_menu))


if __name__ == 'main':
    notification_admin(text=f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
    bot.infinity_polling(timeout=60, long_polling_timeout=60, logger_level=0, interval=0)
else:
    log.cerror(user_id=None, do=f'__name__ == \'main\': {__name__ == 'main'}')
