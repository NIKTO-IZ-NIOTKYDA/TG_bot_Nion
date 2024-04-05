import os
from sqlite3 import sqlite_version
from time import sleep, strftime, localtime
from platform import system, release, python_version

import psutil
import telebot

import db
import config
from loging import loging
from KeyboardsMarkup import *

os.system(config.clear_konsole)

bot = telebot.TeleBot(config.BotToken)


if config.log:
    loging(logger_level='INFO', user_id='none', do='The bot is running . . .')

db.db_connect()

# main fn
def rename(file_name_in: str, file_name_out: str):
    os.system(f'mv {file_name_in} {file_name_out}')

def send_status_text(user_id: int):
    if config.debug:
        loging(logger_level='INFO', user_id=str(user_id), do='Send status . . .')
    bot.send_chat_action(user_id, action='typing')

def newsletter(user_id: int, text: str, i: int, timer: int):
    res = db.return_all_user_id(user_id)
    if res == '[]':
        try:
            bot.send_message(config.main_admin_id, text)
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.main_admin_id}')
        except telebot.apihelper.ApiException:
            loging(logger_level='WARN', user_id=config.main_admin_id, do=f'MAIN Admin {config.main_admin_id} blocked or didn\'t start the bot!')

        loging(logger_level='INFO', user_id=str(user_id), do='Mailing is over')
        bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=markup_start)
    if timer <= 29 and res != '[]':
        try:
            bot.send_message(int(res[i]), str(text))
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {res[i]}')
            i += 1
            timer += 1
            newsletter(user_id=user_id, text=text, i=i, timer=timer)
        except telebot.apihelper.ApiException as Error:
            if Error.result.status_code == 403 or Error.result.status_code == 400:
                loging(logger_level='WARN', user_id=str(res[i]), do=f'User {res[i]} has blocked the bot!')
                # db.remove_user(user_id=str(user_id))
                i += 1
                timer += 1
                newsletter(user_id=user_id, text=text, i=i, timer=timer)
            else:
                loging(logger_level='ERROR', user_id=str(res[i]), do=f'Undefined error !\tERROR: {Error}')
                i += 1
                timer += 1
                newsletter(user_id=user_id, text=text, i=i, timer=timer)
        except IndexError:
            bot.send_message(config.main_admin_id, text)
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.main_admin_id}')
            loging(logger_level='INFO', user_id=str(user_id), do='Mailing is over')
            bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=markup_start)
    else:
        sleep(5)
        timer = 0
        newsletter(user_id=user_id, text=text, i=i, timer=timer)

def send_update_dz(user_id: int, lesson: str):
    if lesson == 'algebra':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Алгебра].', i=0, timer=0)
    elif lesson == 'english_lang_1':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Английский язык (1 группа)].', i=0, timer=0)
    elif lesson == 'english_lang_2':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Английский язык (2 группа)].', i=0, timer=0)
    elif lesson == 'biology':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Биология].', i=0, timer=0)
    elif lesson == 'geography':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [География].', i=0, timer=0)
    elif lesson == 'geometry':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Геометрия].', i=0, timer=0)
    elif lesson == 'computer_science_1':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Информатика (1 группа)].', i=0, timer=0)
    elif lesson == 'computer_science_2':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Информатика (2 группа)].', i=0, timer=0)
    elif lesson == 'story':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [История].', i=0, timer=0)
    elif lesson == 'literature':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Литература].', i=0, timer=0)
    elif lesson == 'music':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Музыка].', i=0, timer=0)
    elif lesson == 'OBZH':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [ОБЖ].', i=0, timer=0)
    elif lesson == 'social_science':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Обществознание].', i=0, timer=0)
    elif lesson == 'native_literature':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Родная литература].', i=0, timer=0)
    elif lesson == 'russian_lang':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Русский язык].', i=0, timer=0)
    elif lesson == 'TBIS':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Теория вероятностей и статистика].', i=0, timer=0)
    elif lesson == 'technology':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Технология].', i=0, timer=0)
    elif lesson == 'physics':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Физика].', i=0, timer=0)
    elif lesson == 'chemistry':
        newsletter(user_id=user_id, text='⚠ Обновлено Д/З [Химия].', i=0, timer=0)

def check_for_admin(user_id: int):
    if user_id == config.main_admin_id:
        loging(logger_level='INFO', user_id=str(user_id), do='Admin check: success')
        return True

    for admin_id in config.admin_id:
        if user_id == admin_id:
            loging(logger_level='INFO', user_id=str(user_id), do='Admin check: success')
            return True

def check_user_in_db(message):
    if db.return_user_authentication(user_id=message.chat.id) == 0:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User authenticated !')
        if message.chat.id != config.main_admin_id:
            db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)
        return 0
    elif db.return_user_authentication(user_id=message.chat.id) == 1:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User unauthenticated !')
        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Add user . . .')
        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'[ ! ] Ошибка аутентификации !\n[ * ] Данные добавлены !\n\nVersion: {config.version}')

def start_bot_notification_admin():
    try:
        loging(logger_level='INFO', user_id='none', do='Sending notifications to admins . . .')
        send_status_text(user_id=config.main_admin_id)
        bot.send_message(config.main_admin_id, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
    except telebot.apihelper.ApiException:
        loging(logger_level='WARN', user_id=config.main_admin_id, do=f'MAIN Admin {config.main_admin_id} blocked or didn\'t start the bot!')
    for admin_id in config.admin_id:
        try:
            bot.send_message(admin_id, f'⚠Бот запущен!⚠')
        except telebot.apihelper.ApiException:
            loging(logger_level='WARN', user_id=admin_id, do=f'Admin {admin_id} blocked or didn\'t start the bot!')

# Command
@bot.message_handler(commands=['start'])
def start(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/start\'')
    if check_for_admin(user_id=message.chat.id):
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Admin pressed \'/start\'')
        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'Добро пожаловать !\nДля доступа к админ панели введите: \n/{config.commands_admin}\n\nVersion: {config.version}', reply_markup=markup_start)
    else:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User (authenticated) pressed \'/start\'')
        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)
        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'Добро пожаловать !\n\nVersion: {config.version}', reply_markup=markup_start)

@bot.message_handler(commands=['dz'])
def dz(message):
    if check_user_in_db(message) == 0:
        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)

@bot.message_handler(commands=['schedule'])
def schedule(message):
    if check_user_in_db(message) == 0:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/schedule\'')
        try:
            photo = open('schedule.jpg', 'rb')
            bot.send_chat_action(message.chat.id, action='upload_photo')
            if check_for_admin(user_id=message.chat.id):
                bot.send_photo(message.chat.id, photo=photo, reply_markup=del_schedule)
            else:
                bot.send_photo(message.chat.id, photo=photo)
        except FileNotFoundError:
            loging(logger_level='WARN', user_id=str(message.chat.id), do='Schedule not found !')
            bot.send_message(message.chat.id, 'Ошибка: файл (расписание) не найден.', reply_markup=markup_start)
            try:
                bot.send_message(config.main_admin_id, 'Файл расписание не найден.\nПожалуйста добавьте расписание !')
            except telebot.apihelper.ApiException:
                loging(logger_level='WARN', user_id=config.main_admin_id, do=f'MAIN Admin {config.main_admin_id} blocked or didn\'t start the bot!')
            for admin_id in config.admin_id:
                try:
                    bot.send_message(admin_id, 'Файл расписание не найден.\nПожалуйста добавьте расписание !')
                except telebot.apihelper.ApiException:
                    loging(logger_level='WARN', user_id=admin_id, do=f'Admin {admin_id} blocked or didn\'t start the bot!')

@bot.message_handler(commands=['call_schedule'])
def call_schedule(message):
    try:
        if check_user_in_db(message) == 0:
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/call_schedule\'')

            call_schedule = '''Урок 1: 8:00   -  8:45
Урок 2: 8:55   -  9:40
Урок 3: 10:00 - 10:45
Урок 4: 11:05 - 11:50
Урок 5: 12:00 - 12:45
Урок 6: 12:55 - 13:40
Урок 7: 13:45 - 14:30
Урок 8: 14:35 - 15:20'''

            lessons = [
                {"start_time": 8_00, "end_time": 8_45},
                {"start_time": 8_55, "end_time": 9_40},
                {"start_time": 10_00, "end_time": 10_45},
                {"start_time": 11_05, "end_time": 11_50},
                {"start_time": 12_00, "end_time": 12_45},
                {"start_time": 12_55, "end_time": 13_40},
                {"start_time": 13_45, "end_time": 14_30},
                {"start_time": 14_35, "end_time": 15_20}
                    ]

            current_time = int(strftime("%H%M", localtime()))

            loging(logger_level='INFO', user_id=str(message.chat.id), do='The enumeration of all lessons and variables has begun')
            for lesson in lessons:
                start_time = lesson["start_time"]
                end_time = lesson["end_time"]

                if start_time <= current_time <= end_time:
                    send_status_text(user_id=message.chat.id)
                    bot.send_message(message.chat.id, f'{call_schedule}\n\nДо конца урока осталось: {divmod(end_time - current_time, 60)[0]} часов и {(end_time - current_time) - (divmod(end_time - current_time, 60)[0] * 60)} минут.')
                    return 0

            if (min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100) >= 0:
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, f'{call_schedule}\n\nСледующий урок через {divmod((min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100), 60)[0]} часов {(min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100) - (divmod((min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100), 60)[0] * 60)} минут')
            elif (min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100) < 0 and config.allow_negative_values_in_call_schedule:
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, f'{call_schedule}\n\nСледующий урок через {((divmod((min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100), 60)[0])*-1)+8} часов {(min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100) - (divmod((min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] // 100 * 60 + min(lessons, key=lambda x: abs(x["start_time"] - current_time))["start_time"] % 100) - (current_time // 100 * 60 + current_time % 100), 60)[0] * 60)} минут')
            else:
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, f'{call_schedule}\n\nУроки закончились на сегодня!')
    except Exception as E:
        print(E)

# Main Admin Panel
@bot.message_handler(commands=['AdminPanel_4qB7cY9jZ2gP'])
def AdminPanel_4qB7cY9jZ2gP(message):
    if message.chat.id == config.main_admin_id:
        loging(logger_level='WARN', user_id=message.chat.id, do='Admin logged into the panel . . .')
        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '''🛠Вы в админ-панели!\nБудте осторожны‼️''', reply_markup=markup_admin_panel)


# Посхалки
@bot.message_handler(commands=['1488'])
def _1488(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_video')
    bot.send_video(message.chat.id, video=open('res/gif/1488.gif', 'rb'), caption='ОСУЖДАЮ НАЦИЗМ ! ! !')

@bot.message_handler(commands=['fah'])
def fah(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/fah.jpg', 'rb'), caption='Марина😏😏😏😏')

@bot.message_handler(commands=['deadp47'])
def deadp47(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/deadp47.jpg', 'rb'), caption='Эй скууууф')

@bot.message_handler(commands=['isaac'])
def isaac(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_video')
    bot.send_video(message.chat.id, video=open('res/gif/isaac.gif', 'rb'), caption='Тут должен был быть коко дамбо но я незнаю как его вставить')

@bot.message_handler(commands=['sigma'])
def sigma(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/sigma.jpg', 'rb'), caption='σ')

@bot.message_handler(commands=['genshin'])
def genshin(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/genshin.jpg', 'rb'), caption='Out for you live, NOW!')

@bot.message_handler(commands=['ambulance'])
def ambulance(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/ambulance.jpg', 'rb'), caption='Ambulance')

@bot.message_handler(commands=['carl_marks'])
def carl_marks(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/carl_marks.jpg', 'rb'), caption='Мой пиар-менеджер - Карл Маркс')

@bot.message_handler(commands=['nik'])
def nik(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/nik.jpg', 'rb'), caption='[данные_удалены]')

@bot.message_handler(commands=['murzik'])
def murzik(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/murzik.jpg', 'rb'), caption='Oh, hello there!')

@bot.message_handler(commands=['spooky'])
def spooky(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/spooky.jpg', 'rb'), caption='You scared?')

@bot.message_handler(commands=['10hours'])
def tenhours(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/10hours.jpg', 'rb'), caption='Я ненавижу рпг макер')

@bot.message_handler(commands=['ded'])
def ded(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/ded.jpg', 'rb'), caption='Мой дедушка прошел афган.....')

@bot.message_handler(commands=['usa'])
def usa(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/usa.jpg', 'rb'), caption='🇺🇸 USA 🇺🇸')

@bot.message_handler(commands=['z'])
def z(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=open('res/photo/z.jpg', 'rb'), caption='🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺 ZZZZZZZZZZZZZZZZZ 🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺')
    

# Other
@bot.message_handler(content_types=['photo'])
def photo(message):
    if check_user_in_db(message) == 0 and check_for_admin(user_id=message.chat.id):
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = 'photo.jpg'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        send_status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, 'Где нужно поставить это фото ?', reply_markup=markup_photo)


# Inline-button
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if db.return_user_authentication(user_id=call.message.chat.id) == 0:
        loging(logger_level='INFO', user_id=str(call.message.chat.id), do=f'Call \'[{call.data}]\'')
        # Show D/Z
        if call.data == 'algebra' or call.data == 'english_lang_1' or call.data == 'english_lang_2' or call.data == 'biology' or call.data == 'geography' or call.data == 'geometry' or call.data == 'computer_science_1' or call.data == 'computer_science_2' or call.data == 'story' or call.data == 'literature' or call.data == 'music' or call.data == 'OBZH' or call.data == 'social_science' or call.data == 'native_literature' or call.data == 'russian_lang' or call.data == 'TBIS' or call.data == 'technology' or call.data == 'physics' or call.data == 'chemistry':
            markup_back = types.InlineKeyboardMarkup(row_width=1)
            url = db.return_url(user_id=call.message.chat.id, lesson=call.data)[0]
            notification_admin = types.InlineKeyboardButton(text='⚠️ Задание не верное или устаревшее ⚠️', callback_data=f'{call.data}_notification_admin')
            del_dz = types.InlineKeyboardButton(text='❌ Удалить Д/З ❌', callback_data=f'{call.data}_del_dz_warn')
            photo = db.return_photo(user_id=call.message.chat.id, lesson=call.data)[0]
            # URL
            if url != 'None':
                url = types.InlineKeyboardButton(text='ГДЗ', url=url)
                back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back')
                if check_for_admin(user_id=call.message.chat.id):
                    markup_back.add(url, del_dz, back)
                else:
                    markup_back.add(url, notification_admin, back)
            else:
                back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back')
                if check_for_admin(user_id=call.message.chat.id):
                    markup_back.add(del_dz, back)
                else:
                    markup_back.add(notification_admin, back)
            # Photo
            if photo != 'None':
                bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
                bot.send_chat_action(call.message.chat.id, action='upload_photo')
                bot.send_photo(call.message.chat.id, photo=open(photo, 'rb'), caption=str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]), reply_markup=markup_back)
            # Default
            else:
                send_status_text(user_id=call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]), reply_markup=markup_back)
        # WARN Del D/Z
        elif call.data == 'algebra_del_dz_warn' or call.data == 'english_lang_1_del_dz_warn' or call.data == 'english_lang_2_del_dz_warn' or call.data == 'biology_del_dz_warn' or call.data == 'geography_del_dz_warn' or call.data == 'geometry_del_dz_warn' or call.data == 'computer_science_1_del_dz_warn' or call.data == 'computer_science_2_del_dz_warn' or call.data == 'story_del_dz_warn' or call.data == 'literature_del_dz_warn' or call.data == 'music_del_dz_warn' or call.data == 'OBZH_del_dz_warn' or call.data == 'social_science_del_dz_warn' or call.data == 'native_literature_del_dz_warn' or call.data == 'russian_lang_del_dz_warn' or call.data == 'TBIS_del_dz_warn' or call.data == 'technology_del_dz_warn' or call.data == 'physics_del_dz_warn' or call.data == 'chemistry_del_dz_warn':
            markup_del_dz_warn = types.InlineKeyboardMarkup(row_width=1)
            yes = types.InlineKeyboardButton(text='✅ Да ✅', callback_data=f'{call.data.replace("_warn", "")}')
            no = types.InlineKeyboardButton(text='❌ Нет ❌', callback_data='no_del_dz')
            markup_del_dz_warn.add(yes, no)
            send_status_text(user_id=call.message.chat.id)
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'⚠ Вы уверены ?\n\nД/З: {db.return_dz(user_id=call.message.chat.id, lesson=call.data.replace("_del_dz_warn", ""))[0]}', reply_markup=markup_del_dz_warn)
            except Exception as Error:
                loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Error in edit_message_text')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=f'⚠ Вы уверены ?\n\nД/З: {db.return_dz(user_id=call.message.chat.id, lesson=call.data.replace("_del_dz_warn", ""))[0]} + Photo', reply_markup=markup_del_dz_warn)
        # Del D/Z
        elif call.data == 'algebra_del_dz' or call.data == 'english_lang_1_del_dz' or call.data == 'english_lang_2_del_dz' or call.data == 'biology_del_dz' or call.data == 'geography_del_dz' or call.data == 'geometry_del_dz' or call.data == 'computer_science_1_del_dz' or call.data == 'computer_science_2_del_dz' or call.data == 'story_del_dz' or call.data == 'literature_del_dz' or call.data == 'music_del_dz' or call.data == 'OBZH_del_dz' or call.data == 'social_science_del_dz' or call.data == 'native_literature_del_dz' or call.data == 'russian_lang_del_dz' or call.data == 'TBIS_del_dz' or call.data == 'technology_del_dz' or call.data == 'physics_del_dz' or call.data == 'chemistry_del_dz':
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется удаление, пожалуйста, подождите . . .')
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_del_dz", ""), dz='Не добавлено домашнее задание =(')
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_del_dz", ""), path='None')
            try:
                os.remove('photo/' + call.data.replace("_del_dz", "") + '.jpg')
            except FileNotFoundError:
                pass
            db.replace_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace("_del_dz", ""))
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do=f'Admin deleted dz \'{call.data.replace("_del_dz", "")}\'')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        # Notification admin
        elif call.data == 'algebra_notification_admin' or call.data == 'english_lang_1_notification_admin' or call.data == 'english_lang_2_notification_admin' or call.data == 'biology_notification_admin' or call.data == 'geography_notification_admin' or call.data == 'geometry_notification_admin' or call.data == 'computer_science_1_notification_admin' or call.data == 'computer_science_2_notification_admin' or call.data == 'story_notification_admin' or call.data == 'literature_notification_admin' or call.data == 'music_notification_admin' or call.data == 'OBZH_notification_admin' or call.data == 'social_science_notification_admin' or call.data == 'native_literature_notification_admin' or call.data == 'russian_lang_notification_admin' or call.data == 'TBIS_notification_admin' or call.data == 'technology_notification_admin' or call.data == 'physics_notification_admin' or call.data == 'chemistry_notification_admin':
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do=f'User: {call.message.chat.id} requested a D/Z update')
            less = call.data.replace("_notification_admin", "")

            def enter_message(call):
                send_status_text(user_id=call.message.chat.id)
                msg = bot.send_message(call.message.chat.id, '⚠️ Введите комментарий к запросу в нём можно указать на ошибку или предложить правильное Д/З', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(msg, start_mailing_admin)

            def start_mailing_admin(call):
                if call.text[0] == '/' or call.text == 'Домашнее задание 📚' or call.text == 'Расписание 📑' or call.text == 'Расписание звонков 🕝':
                    send_status_text(user_id=call.chat.id)
                    bot.send_message(call.chat.id, '⚠️ Отправка прервана вы перенаправлены в главное меню.', reply_markup=markup_start)
                else:
                    try:
                        bot.send_message(config.main_admin_id, f'⚠️ Пользователь: {call.chat.id} уведомил вас в неактуальности Д/З по {less}\n\nКомментарий: {call.text}')
                    except telebot.apihelper.ApiException:
                        loging(logger_level='WARN', user_id=config.main_admin_id, do=f'MAIN Admin {config.main_admin_id} blocked or didn\'t start the bot!')
                    for admin_id in config.admin_id:
                        try:
                            bot.send_message(admin_id, f'⚠️ Пользователь: {call.chat.id} уведомил вас в неактуальности Д/З по {less}\n\nКомментарий: {call.text}')
                        except telebot.apihelper.ApiException:
                            loging(logger_level='WARN', user_id=admin_id, do=f'Admin {admin_id} blocked or didn\'t start the bot!')
                    send_status_text(user_id=call.chat.id)
                    bot.send_message(call.chat.id, '✅ Отчёт успешно отправлен. Извините за неудобства.')
            enter_message(call)
        # Back
        elif call.data == 'back':
            try:
                send_status_text(user_id=call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет', reply_markup=markup_dz)
            except telebot.apihelper.ApiException as Error:
                if Error.result.status_code == 400:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_status_text(user_id=call.message.chat.id)
                    bot.send_message(call.message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)
        # Del schedule
        elif call.data == 'del_schedule':
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется удаление, пожалуйста, подождите . . .')
            try:
                os.remove('schedule.jpg')
            except FileNotFoundError:
                pass
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do=f'Admin deleted schedule')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        # § (Paragraph)
        elif call.data == 'paragraph':
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '§')
        # No del D/Z
        elif call.data == 'no_del_dz':
            send_status_text(user_id=call.message.chat.id)
            bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        # Replace D/Z
        elif call.data == 'algebra_update' or call.data == 'english_lang_1_update' or call.data == 'english_lang_2_update' or call.data == 'biology_update' or call.data == 'geography_update' or call.data == 'geometry_update' or call.data == 'computer_science_1_update' or call.data == 'computer_science_2_update' or call.data == 'story_update' or call.data == 'literature_update' or call.data == 'music_update' or call.data == 'OBZH_update' or call.data == 'social_science_update' or call.data == 'native_literature_update' or call.data == 'russian_lang_update' or call.data == 'TBIS_update' or call.data == 'technology_update' or call.data == 'physics_update' or call.data == 'chemistry_update':
            bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='None')
            try:
                os.remove('photo/' + call.data.replace("_update", "") + '.jpg')
            except FileNotFoundError:
                pass
            db.replace_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            send_update_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""))
        # Replace D/Z + photo
        elif call.data == 'algebra_update_p' or call.data == 'english_lang_1_update_p' or call.data == 'english_lang_2_update_p' or call.data == 'biology_update_p' or call.data == 'geography_update_p' or call.data == 'geometry_update_p' or call.data == 'computer_science_1_update_p' or call.data == 'computer_science_2_update_p' or call.data == 'story_update_p' or call.data == 'literature_update_p' or call.data == 'music_update_p' or call.data == 'OBZH_update_p' or call.data == 'social_science_update_p' or call.data == 'native_literature_update_p' or call.data == 'russian_lang_update_p' or call.data == 'TBIS_update_p' or call.data == 'technology_update_p' or call.data == 'physics_update_p' or call.data == 'chemistry_update_p':
            bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='None', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            send_update_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""))
        # Replace URL
        elif call.data == 'algebra_url' or call.data == 'english_lang_1_url' or call.data == 'english_lang_2_url' or call.data == 'biology_url' or call.data == 'geography_url' or call.data == 'geometry_url' or call.data == 'computer_science_1_url' or call.data == 'computer_science_2_url' or call.data == 'story_url' or call.data == 'literature_url' or call.data == 'music_url' or call.data == 'OBZH_url' or call.data == 'social_science_url' or call.data == 'native_literature_url' or call.data == 'russian_lang_url' or call.data == 'TBIS_url' or call.data == 'technology_url' or call.data == 'physics_url' or call.data == 'chemistry_url':
            bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            send_status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
    else:
        loging(logger_level='INFO', user_id=str(call.message.chat.id), do='User unauthenticated ! (in callback_handler)')
        send_status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '[!] Критическая ошибка аутентификации !\nПожалуйста введите команду /start')


# Text
@bot.message_handler(content_types=['text'])
def logic(message):
    if check_user_in_db(message) == 0:
        loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
        if message.text == 'Домашнее задание 📚':
            dz(message)
        elif message.text == 'Расписание 📑':
            schedule(message)
        elif message.text == 'Расписание звонков 🕝':
            call_schedule(message)
        # Update photo
        elif message.text == 'Расписание' and check_for_admin(user_id=message.chat.id):
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Start uploading photos . . .')
            rename(file_name_in='photo.jpg', file_name_out='schedule.jpg')
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Successfully !')
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '✅ Расписание сохранено!')
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(message.chat.id), do='Start of the mailing list')
            send_status_text(user_id=message.chat.id)
            newsletter(user_id=message.chat.id, text='⚠ Обновлено расписание.', i=0, timer=0)
        elif message.text == 'Д/З' and check_for_admin(user_id=message.chat.id):
            def enter_dz(message):
                send_status_text(user_id=message.chat.id)
                msg = bot.send_message(message.chat.id, 'Введите Д/З', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(msg, enter_lessons)

            def enter_lessons(message):
                global input_text
                input_text = message.text
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update_p)
            enter_dz(message)
        elif message.text == '⬅️ Назад':
            try:
                os.remove('photo.jpg')
            except Exception:
                pass
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, 'Вы вернулись назад', reply_markup=markup_start)
        # Update dz or url
        elif message.text == 'Д/3' and message.chat.id == config.main_admin_id:
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update)
        elif message.text == 'ГДЗ' and message.chat.id == config.main_admin_id:
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить ГДЗ', reply_markup=markup_url)
        # Посхало
        elif message.text == 'Оля' or message.text == 'оля':
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.send_photo(message.chat.id, photo=open('res/photo/ola.jpg', 'rb'), caption='ниф ниф или нуф нуф?')
        # Main Admin Panel
        elif message.text == 'Рассылка✉️' and message.chat.id == config.main_admin_id:
            def enter_message(message):
                msg = bot.send_message(message.chat.id, '⚠️ Введите сообщение', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(msg, start_mailing)

            def start_mailing(message):
                config.input_text_mailing = message.text
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, f'<u><b>‼️ВЫ ТОЧНО ХОТИТЕ ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ ПОЛЬЗОВАТЕЛЯМ⁉️</b></u>\nТЕКСТ СООБЩЕНИЯ:\n{config.input_text_mailing}', parse_mode='html', reply_markup=markup_chack_mailing)

            enter_message(message)
        elif message.text == '✅ YES ✅' and message.chat.id == config.main_admin_id:
            loging(logger_level='WARN', user_id=message.chat.id, do='Start of the mailing list')
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '✅ Рассылка началась!', reply_markup=types.ReplyKeyboardRemove())
            try:
                newsletter(user_id=message.chat.id, text=config.input_text_mailing, i=0, timer=0)
            except Exception as E:
                loging(logger_level='ERROR', user_id=str(message.chat.id), do=f'Error: {E}')
        elif message.text == '❌ NO ❌' and message.chat.id == config.main_admin_id:
            config.input_text_mailing = [None]
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '✅Вы вернулись назад!', reply_markup=markup_admin_panel)
        elif message.text == 'Перезагрузка 🔄' and message.chat.id == config.main_admin_id:
            loging(logger_level='WARN', user_id=message.chat.id, do='Rebooting . . .')
            newsletter(user_id=message.chat.id, text='⚠️ Бот будет перезагружен !\n\nПодождите ~20 секунд.', i=0, timer=0)
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '⚠️ Бот будет перезагружен !\n\nПодождите ~20 секунд.')
            db.db_stop(user_id=message.chat.id)
            newsletter(user_id=message.chat.id, text='⚠ База данных отключена !', i=0, timer=0)
            bot.stop_bot()
            os.system(config.reboot_command)
        elif message.text == 'Выключение сервера ‼️' and message.chat.id == config.main_admin_id:
            loging(logger_level='WARN', user_id=message.chat.id, do='Shutdown . . .')
            newsletter(user_id=message.chat.id, text='⚠️ Выключение сервера . . .', i=0, timer=0)
            db.db_stop(user_id=message.chat.id)
            newsletter(user_id=message.chat.id, text='⚠ База данных отключена !', i=0, timer=0)
            bot.stop_bot()
            os.system(config.shutdown_command)
        elif message.text == 'Бэкап базы данных 📑' and message.chat.id == config.main_admin_id:
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin performs db backup . . .')
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '✅ Отправляю . . .')
            loging(logger_level='WARN', user_id=message.chat.id, do='Sending a database backup')
            bot.send_chat_action(message.chat.id, 'upload_document')
            bot.send_document(message.chat.id, document=open(config.name_database, 'rb'))
        elif message.text == 'Статус сервера 🛠️' and message.chat.id == config.main_admin_id:
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Аdmin requested a server status report, generation . . .')
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: SystemName')
            SystemName = str(system())
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: SystemRelease')
            SystemRelease = str(release())
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: PythonVersion')
            PythonVersion = str(python_version())
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: SQLite3Version')
            SQLite3Version = str(sqlite_version)
            # Загруженость
            # CPU
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: CPUs, CPU_stats')
            cpu = psutil.cpu_times()
            cpu_stats = psutil.cpu_stats()
            # Memory
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: Memory_Virtual, Memory_Swap')
            Memory_Virtual = psutil.virtual_memory()
            Memory_Swap = psutil.swap_memory()
            # Disks
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: Disks')
            Disks = psutil.disk_io_counters()
            # Network
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: Network')
            Network = psutil.net_if_addrs()
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating a report based on the data received . . .')
            info = f'''OS: {SystemName} {SystemRelease}
Python: {PythonVersion} Version
SQLite3: {SQLite3Version} Version'''
            info_d = f'''Загруженость:
#~CPU~#
CPU: {cpu}
CPU Stats: {cpu_stats}
#~MEMORY~#
Memory Virtual: = {Memory_Virtual}
Memory Swap: = {Memory_Swap}
#~DISKS~#
Disks: {Disks}
#~NETWORK~#
Network: = {Network}'''
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Successfully !')
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, info)
            send_status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, info_d)
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Report Sent !')
        else:
            if message.chat.id == config.main_admin_id:
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, 'Где нужно поставить этот текст ?', reply_markup=markup_update_dz_or_gdz)
                global input_text
                input_text = message.text
            elif check_for_admin(user_id=message.chat.id):
                loging(logger_level='INFO', user_id=str(message.chat.id), do='User replase D/Z')
                input_text = message.text
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update)
            else:
                loging(logger_level='INFO', user_id=str(message.chat.id), do=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')
                send_status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌')


if __name__ == '__main__':
    start_bot_notification_admin()
    bot.infinity_polling(long_polling_timeout=60, logger_level=0, interval=0)  # Запуск бота
