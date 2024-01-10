import os
from time import sleep
from sqlite3 import sqlite_version

import psutil
import telebot
import platform

import db
import config
from texts import *
from loging import loging
from KeyboardsMarkup import *

os.system(config.ClearKonsole)

def rename(file_name_in: str, file_name_out: str):
    os.system(f'mv {file_name_in} {file_name_out}')


bot = telebot.TeleBot(config.BotToken)

if config.log:
    print('[FORMAN]   [ID]             [TIME]    [DO]')
loging(logger_level='INFO', user_id='nope', do='The bot is running . . .')

db.db_connect()


def status_text(user_id: int):
    loging(logger_level='INFO', user_id=str(user_id), do='Send status . . .')
    db.update_latest_posts_time(user_id=user_id)
    bot.send_chat_action(user_id, action='typing')

def send_message(user_id: int, text: str, i: int):
    res = db.return_all_user_id()
    if res == '[]':
        bot.send_message(config.admin_id_1, text)
        loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.admin_id_1}')
        loging(logger_level='INFO', user_id=str(user_id), do='Mailing is over')
        bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=markup_start)
    if i <= 29:
        try:
            bot.send_message(int(res[i]), str(text))
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {res[i]}')
            i += 1
            send_message(user_id=user_id, text=text, i=i)
        except telebot.apihelper.ApiException as Error:
            if Error.result.status_code == 403 or Error.result.status_code == 400:
                loging(logger_level='WARN', user_id=str(res[i]), do=f'User {res[i]} has blocked the bot!')
                # db.remove_user(user_id=str(user_id))
                i += 1
                send_message(user_id=user_id, text=text, i=i)
            else:
                loging(logger_level='ERROR', user_id=str(res[i]), do=f'Undefined error !\tERROR: {Error}')
        except IndexError:
            bot.send_message(config.admin_id_1, text)
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.admin_id_1}')
            loging(logger_level='INFO', user_id=str(user_id), do='Mailing is over')
            bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=markup_start)
    else:
        sleep(1)

def check_user(user_id: int):
    if db.return_user_authentication(user_id=user_id) == '0':
        loging(logger_level='INFO', user_id=str(user_id), do='User authenticated !')
        return '0'
    elif db.return_user_authentication(user_id=user_id) == '1':
        loging(logger_level='INFO', user_id=str(user_id), do='User unauthenticated !')
        status_text(user_id=user_id)
        bot.send_message(user_id, 'Ошибка аутентификации !\nДобавьте необходимые данные для корректной работы бота.', reply_markup=markup_send_nummer)
    else:
        loging(logger_level='ERROR', user_id='nope', do='Unknown authentication error !')
        status_text(user_id=user_id)
        bot.send_message(user_id, 'Unknown authentication error !')

# Command
@bot.message_handler(commands=['start'])
def start(message):
    if check_user(user_id=message.chat.id) == '0':
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/start\'')
        if message.chat.id == config.admin_id_1:
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Admin pressed \'/start\'')
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, f'Для доступа к админ панели введите: \n/{config.commands_admin}')
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, TEXT_start, reply_markup=markup_start)
        else:
            loging(logger_level='INFO', user_id=str(message.chat.id), do='User (authenticated) pressed \'/start\'')
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, TEXT_start, reply_markup=markup_start)
@bot.message_handler(commands=['dz'])
def dz(message):
    if check_user(user_id=message.chat.id) == '0':
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)

@bot.message_handler(commands=['schedule'])
def schedule(message):
    if check_user(user_id=message.chat.id) == '0':
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/schedule\'')
        try:
            photo = open('schedule.jpg', 'rb')
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.send_photo(message.chat.id, photo=photo)
        except FileNotFoundError:
            loging(logger_level='WARN', user_id=str(message.chat.id), do='Schedule not found !')
            bot.send_message(message.chat.id, 'Ошибка: файл (расписание) не найден.', reply_markup=markup_start)
            bot.send_message(config.admin_id_1, 'Файл расписание не найден.\nПожалуйста добавьте расписание !')
            # bot.send_message(config.admin_id_2, 'Расписание не найден.\nПожалуйста добавьте расписание !')
            # bot.send_message(config.admin_id_3, 'Расписание не найден.\nПожалуйста добавьте расписание !')
            bot.send_message(config.user_schedule_1, 'Расписание не найден.\nПожалуйста добавьте расписание !')
            # bot.send_message(config.user_schedule2, 'Расписание не найден.\nПожалуйста добавьте расписание !')

@bot.message_handler(commands=['call_schedule'])
def call_schedule(message):
    if check_user(user_id=message.chat.id) == '0':
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/call_schedule\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, TEXT_call_schedule)

@bot.message_handler(commands=['update_date_db'])
def update_date_db(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/update_date_db\'')
    if message.chat.id == config.admin_id_1:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Admin pressed \'/update_date_db\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, ' Вы не можете зарегистрированы т. к. являетесь админом', reply_markup=markup_start)
    else:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User pressed \'/update_date_db\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '⚙ Отправьте свой номер телефона.', reply_markup=markup_send_nummer)

# Other
@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'[contact]\'')
        db.db_add_data(user_id=message.chat.id, username=message.from_user.username, user_phone_number=message.contact.phone_number, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, user_lang=message.from_user.language_code)
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '✅ Данные успешно добавлены/обновлены в базе данных')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, TEXT_start, reply_markup=markup_start)

@bot.message_handler(content_types=['photo'])
def photo(message):
    if check_user(user_id=message.chat.id) == '0':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.user_dz_1 or message.chat.id == config.user_dz_2 or message.chat.id == config.user_dz_3 or message.chat.id == config.user_dz_4 or message.chat.id == config.user_schedule_1 or message.chat.id == config.user_schedule_2:
            status_text(user_id=message.chat.id)
            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = 'photo.jpg'
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, 'Где нужно поставить это фото ?', reply_markup=markup_photo)

# Inline-button
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if check_user(user_id=call.message.chat.id) == '0':
        loging(logger_level='INFO', user_id=str(call.message.chat.id), do=f'Call \'[{call.data}]\'')
        # Show D/Z
        if call.data == 'algebra' or call.data == 'english_lang_1' or call.data == 'english_lang_2' or call.data == 'biology' or call.data == 'geography' or call.data == 'geometry' or call.data == 'computer_science_1' or call.data == 'computer_science_2' or call.data == 'story' or call.data == 'literature' or call.data == 'music' or call.data == 'OBZH' or call.data == 'social_science' or call.data == 'native_literature' or call.data == 'russian_lang' or call.data == 'TBIS' or call.data == 'technology' or call.data == 'physics' or call.data == 'chemistry':
            try:
                markup_back = types.InlineKeyboardMarkup(row_width=1)
                url = db.return_url(user_id=call.message.chat.id, lesson=call.data)[0]
                if url != 'Nope':
                    url = types.InlineKeyboardButton(text='ГДЗ', url=url)
                    back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back')
                    markup_back.add(url, back)
                else:
                    back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back')
                    markup_back.add(back)

                photo = db.return_photo(user_id=call.message.chat.id, lesson=call.data)[0]
                if photo != 'Nope':
                    bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
                    bot.send_chat_action(call.message.chat.id, action='upload_photo')
                    bot.send_photo(call.message.chat.id, photo=open(photo, 'rb'), caption=str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]), reply_markup=markup_back)
                else:
                    status_text(user_id=call.message.chat.id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]), reply_markup=markup_back)
            except Exception as e:
                print(e)
        elif call.data == 'back':
            try:
                status_text(user_id=call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👇 Выберете предмет', reply_markup=markup_dz)
            except telebot.apihelper.ApiException as Error:
                if Error.result.status_code == 400:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    status_text(user_id=call.message.chat.id)
                    bot.send_message(call.message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)
        # Replace D/Z
        elif call.data == 'algebra_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Алгебра].', i=0)
        elif call.data == 'english_lang_1_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Английский язык (1 группа)].', i=0)
        elif call.data == 'english_lang_2_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Английский язык (2 группа)].', i=0)
        elif call.data == 'biology_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Биология].', i=0)
        elif call.data == 'geography_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [География].', i=0)
        elif call.data == 'geometry_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Геометрия].', i=0)
        elif call.data == 'computer_science_1_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Информатика (1 группа)].', i=0)
        elif call.data == 'computer_science_2_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Информатика (2 группа)].', i=0)
        elif call.data == 'story_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [История].', i=0)
        elif call.data == 'literature_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Литература].', i=0)
        elif call.data == 'music_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Музыка].', i=0)
        elif call.data == 'OBZH_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [ОБЖ].', i=0)
        elif call.data == 'social_science_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Обществознание].', i=0)
        elif call.data == 'native_literature_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Родноя литература].', i=0)
        elif call.data == 'russian_lang_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Русский язык].', i=0)
        elif call.data == 'TBIS_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Теория вероятностей и статистика].', i=0)
        elif call.data == 'technology_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Технология].', i=0)
        elif call.data == 'physics_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Физика].', i=0)
        elif call.data == 'chemistry_update':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), path='Nope')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Химия].', i=0)
        # Replace D/Z + photo
        elif call.data == 'algebra_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Алгебра].', i=0)
        elif call.data == 'english_lang_1_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Английский язык (1 группа)].', i=0)
        elif call.data == 'english_lang_2_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
        elif call.data == 'biology_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Биология].', i=0)
        elif call.data == 'geography_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [География].', i=0)
        elif call.data == 'geometry_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Геометрия].', i=0)
        elif call.data == 'computer_science_1_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Информатика (1 группа)].', i=0)
        elif call.data == 'computer_science_2_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Информатика (2 группа)].', i=0)
        elif call.data == 'story_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [История].', i=0)
        elif call.data == 'literature_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Литература].', i=0)
        elif call.data == 'music_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Музыка].', i=0)
        elif call.data == 'OBZH_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [ОБЖ].', i=0)
        elif call.data == 'social_science_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Обществознание].', i=0)
        elif call.data == 'native_literature_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Родноя литература].', i=0)
        elif call.data == 'russian_lang_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Русский язык].', i=0)
        elif call.data == 'TBIS_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Теория вероятностей и статистика].', i=0)
        elif call.data == 'technology_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Технология].', i=0)
        elif call.data == 'physics_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Физика].', i=0)
        elif call.data == 'chemistry_update_p':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), dz=input_text)
            db.replace_photo(user_id=call.message.chat.id, lesson=call.data.replace("_update_p", ""), path='photo/' + call.data.replace("_update_p", "") + '.jpg')
            rename(file_name_in='photo.jpg', file_name_out='photo/' + call.data.replace("_update_p", "") + '.jpg')
            db.replace_url(user_id=call.message.chat.id, url='Nope', lesson=call.data.replace("_update_p", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
            bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
            loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
            status_text(user_id=call.message.chat.id)
            send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Химия].', i=0)
        # Replace URL
        elif call.data == 'algebra_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'english_lang_1_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'english_lang_2_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'biology_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'geography_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'geometry_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'computer_science_1_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'computer_science_2_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'story_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'literature_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'music_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'OBZH_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'social_science_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'native_literature_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'russian_lang_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'TBIS_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'technology_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'physics_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')
        elif call.data == 'chemistry_url':
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚙️ Выполняется замена, пожалуйста, подождите . . .', reply_markup=types.ReplyKeyboardRemove())
            db.replace_url(user_id=call.message.chat.id, url=input_text, lesson=call.data.replace("_url", ""))
            loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
            status_text(user_id=call.message.chat.id)
            bot.send_message(call.message.chat.id, '✅ Успешно !')

# Text
@bot.message_handler(content_types=['text'])
def logic(message):
    if check_user(user_id=message.chat.id) == '0':
        loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
        if message.text == 'Домашнее задание 📚':
            dz(message)
        elif message.text == 'Расписание 📑':
            schedule(message)
        elif message.text == 'Расписание звонков 🕝':
            call_schedule(message)
        # Update photo
        elif message.text == 'Расписание':
            if message.chat.id == config.admin_id_1 or message.chat.id == config.user_schedule_1 or message.chat.id == config.user_schedule_2:
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Start uploading photos . . .')
                rename(file_name_in='photo.jpg', file_name_out='schedule.jpg')
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Successfully !')
                status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '✅ Расписание сохранено!')
                status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
                loging(logger_level='WARN', user_id=str(message.chat.id), do='Start of the mailing list')
                status_text(user_id=message.chat.id)
                send_message(user_id=message.chat.id, text='⚠ Обновлено расписание.', i=0)
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        elif message.text == 'Д/З':
            if message.chat.id == config.admin_id_1 or message.chat.id == config.user_dz_1 or message.chat.id == config.user_dz_2 or message.chat.id == config.user_dz_3 or message.chat.id == config.user_dz_4:
                def enter_dz(message):
                    msg = bot.send_message(message.chat.id, 'Введите Д/З', reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(msg, enter_lessons)

                def enter_lessons(message):
                    global input_text
                    input_text = message.text
                    bot.send_message(message.chat.id, 'Выберете урок:', reply_markup=markup_dz_update_p)
                enter_dz(message)
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        elif message.text == '⬅️ Назад':
            try:
                os.system('rm photo.jpg')
            except Exception:
                pass
            bot.send_message(message.chat.id, 'Вы вернулись назад', reply_markup=markup_start)
        # Update dz or url
        elif message.text == 'Д/3':
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update)
        elif message.text == 'ГДЗ':
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить ГДЗ', reply_markup=markup_url)
        # Admin Panel
        elif message.text == f'/{config.commands_admin}':
            if message.chat.id == config.admin_id_1:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=message.chat.id, do='Admin logged into the panel . . .')
                bot.send_message(message.chat.id, '''🛠Вы в админ-панели!\nБудте осторожны‼️''', reply_markup=markup_admin_panel)
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        elif message.text == 'Рассылка✉️':
            if message.chat.id == config.admin_id_1:
                def enter_message(message):
                    msg = bot.send_message(message.chat.id, '⚠️ Введите сообщение', reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(msg, start_mailing)

                def start_mailing(message):
                    global input_text_mailing
                    input_text_mailing = message.text
                    status_text(user_id=message.chat.id)
                    bot.send_message(message.chat.id, f'<u><b>‼️ВЫ ТОЧНО ХОТИТЕ ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ ПОЛЬЗОВАТЕЛЯМ⁉️</b></u>\nТЕКСТ СООБЩЕНИЯ:\n{input_text_mailing}', parse_mode='html', reply_markup=markup_chack_mailing)
                enter_message(message)
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        elif message.text == '✅ YES ✅':
            loging(logger_level='WARN', user_id=message.chat.id, do='Start of the mailing list')
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '✅ Рассылка началась!', reply_markup=types.ReplyKeyboardRemove())
            send_message(user_id=message.chat.id, text=input_text_mailing,  i=0)
        elif message.text == '❌ NO ❌':
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '✅Вы вернулись назад!', reply_markup=markup_start)
        elif message.text == 'Перезагрузка 🔄':
            if message.chat.id == config.admin_id_1:
                status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '⚠️ Бот будет перезагружен !\n\nПодождите ~20 секунд.')
                db.db_stop(user_id=message.chat.id)
                sleep(1)
                bot.stop_bot()
                os.system(config.reboot_command)
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        elif message.text == 'Бэкап базы данных 📑':
            if message.chat.id == config.admin_id_1:
                db.db_backup()
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=message.chat.id, do='Admin performs db backup . . .')
                bot.send_message(message.chat.id, '✅Бэкап базы данных готов!\nОтправляю . . .')
                loging(logger_level='WARN', user_id=message.chat.id, do='The backup copy of the database is ready, I’m sending it. . .')
                bot.send_chat_action(message.chat.id, 'upload_document')
                bot.send_document(message.chat.id, document=open('sql_damp.txt', 'rb'))
                sleep(1)
                loging(logger_level='WARN', user_id=message.chat.id, do='Deleting a database backup . . .')
                os.system('rm sql_damp.txt')
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        elif message.text == 'Статус сервера 🛠️':
            if message.chat.id == config.admin_id_1:
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Аdmin requested a server status report, generation . . .')
                status_text(user_id=message.chat.id)
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: SystemName')
                SystemName = str(platform.system())
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: SystemRelease')
                SystemRelease = str(platform.release())
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: PythonVersion')
                PythonVersion = str(platform.python_version())
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: SQLite3Version')
                SQLite3Version = str(sqlite_version)
                # Загруженость
                # CPU
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: CPU, CPU_stats')
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
SQLite3: {SQLite3Version} Version
~~~~~~~~~~~~~~~~~
Загруженость:
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
                status_text(user_id=message.chat.id)
                loging(logger_level='INFO', user_id=str(message.chat.id), do='Report Sent !')
                bot.send_message(message.chat.id, info)
            else:
                status_text(user_id=message.chat.id)
                loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
                bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
        else:
            if message.chat.id == config.admin_id_1:
                bot.send_message(message.chat.id, 'Где нужно поставить этот текст ?', reply_markup=markup_update_dz_or_gdz)
                status_text(user_id=message.chat.id)
                global input_text
                input_text = message.text
            elif message.chat.id == config.user_dz_1 or message.chat.id == config.user_dz_2 or message.chat.id == config.user_dz_3 or message.chat.id == config.user_dz_4:
                loging(logger_level='INFO', user_id=str(message.chat.id), do='User replase D/Z')
                status_text(user_id=message.chat.id)
                input_text = message.text
                bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update)
            else:
                loging(logger_level='INFO', user_id=str(message.chat.id), do=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')
                status_text(user_id=message.chat.id)
                bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌')


loging(logger_level='INFO', user_id='nope', do='Sending notifications to admins . . .')

bot.send_message(config.admin_id_1, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')

if __name__ == '__main__':
    bot.infinity_polling(long_polling_timeout=60, logger_level=1, interval=0)  # Запуск бота
