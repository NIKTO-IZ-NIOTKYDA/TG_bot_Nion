import os
import psutil
import platform
from time import sleep
from sqlite3 import sqlite_version

import telebot

import db
import config
from texts import *
from loging import loging
from KeyboardsMarkup import *

os.system('clear')  # Clear Konsole
bot = telebot.TeleBot(config.BotToken)

print('[FORMAN]   [ID]             [TIME]    [DO]')
loging(logger_level='INFO', user_id='nope', do='The bot is running . . .')
sleep(1)

db.db_connect()

def status_text(user_id: int):
    loging(logger_level='INFO', user_id=str(user_id), do='Send status . . .')
    db.update_latest_posts_time(user_id=user_id)
    bot.send_chat_action(user_id, action='typing')

def send_message(user_id: int, text: str, i: int):
    if i <= 29:
        res = db.return_all_user_id()
        try:
            bot.send_message(int(res[i]), str(text))
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {res[i]}')
            i += 1
            send_message(user_id=user_id, text=text, i=i)
        except telebot.apihelper.ApiException as Error:
            if Error.result.status_code == 403 or Error.result.status_code == 400:
                loging(logger_level='WARN', user_id=str(res[i]), do=f'User {res[i]} has blocked the bot!')
                # db.remove_user_id(user_id=str(user_id))
                i += 1
                send_message(user_id=user_id, text=text, i=i)
            else:
                loging(logger_level='ERROR', user_id=str(res[i]), do=f'Undefined error !\tERROR: {Error}')
        except IndexError:
            sleep(1)
            bot.send_message(config.admin_id_1, text)
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.admin_id_1}')
            sleep(1)
            bot.send_message(config.admin_id_2, text)
            loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.admin_id_2}')
            sleep(1)
            # bot.send_message(config.admin_id_3, text)
            # loging(logger_level='INFO', user_id=str(user_id), do=f'Sent: {config.admin_id_3}')
            loging(logger_level='INFO', user_id=str(user_id), do='Mailing is over')
            bot.send_message(user_id, '✅ Рассылка закончена!', reply_markup=markup_start)
    else:
        sleep(2)

# Command
@bot.message_handler(commands=['dz'])
def dz(message):
    status_text(user_id=message.chat.id)
    bot.send_message(message.chat.id, '👇 Выберете предмет', reply_markup=markup_dz)

@bot.message_handler(commands=['schedule'])
def schedule(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/schedule\'')
    try:
        photo = open('schedule.jpg', 'rb')
    except FileNotFoundError:
        loging(logger_level='WARN', user_id=str(message.chat.id), do='Schedule not found !')
        bot.send_message(message.chat.id, 'Ошибка: файл (расписание) не найден.', reply_markup=markup_start)
        bot.send_message(config.admin_id_1, 'Расписание не найден.\nПожалуйста добавьте расписание !')
        # bot.send_message(config.admin_id_2, 'Расписание не найден.\nПожалуйста добавьте расписание !')
        # bot.send_message(config.admin_id_3, 'Расписание не найден.\nПожалуйста добавьте расписание !')
        # bot.send_message(config.user_schedule1, 'Расписание не найден.\nПожалуйста добавьте расписание !')
        # bot.send_message(config.user_schedule2, 'Расписание не найден.\nПожалуйста добавьте расписание !')
    bot.send_chat_action(message.chat.id, action='upload_photo')
    bot.send_photo(message.chat.id, photo=photo)

@bot.message_handler(commands=['call_schedule'])
def call_schedule(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/call_schedule\'')
    status_text(user_id=message.chat.id)
    bot.send_message(message.chat.id, TEXT_call_schedule)

@bot.message_handler(commands=['start'])
def start(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/start\'')
    if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Admin pressed \'/start\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, f'Для доступа к админ панели введите: \n/{config.commands_admin}')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, TEXT_start, reply_markup=markup_start)
    elif db.db_table_bool_return(user_id=message.chat.id) == '(1,)':
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User (authenticated) pressed \'/start\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, TEXT_start, reply_markup=markup_start)
    else:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User (unauthenticated) pressed \'/start\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, 'Add the necessary data for the bot to work properly.\n⚙ Send your phone number to continue.', reply_markup=markup_send_nummer)

@bot.message_handler(commands=['update_date_db'])
def update_date_db(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'/update_date_db\'')
    if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Admin pressed \'/update_date_db\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, ' Вы не можете зарегистрированы т. к. являетесь админом', reply_markup=markup_start)
    else:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='User pressed \'/update_date_db\'')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '⚙ Send your phone number to continue.', reply_markup=markup_send_nummer)

# Other
@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Received \'[contact]\'')
        db.db_table_val(user_id=message.chat.id, username=message.from_user.username, user_phone_number=message.contact.phone_number, user_name=message.from_user.first_name, user_surname=message.from_user.last_name,  user_lang=message.from_user.language_code)
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '✅ Data has been successfully added/updated in the database')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, TEXT_start, reply_markup=markup_start)

@bot.message_handler(content_types=['photo'])
def photo(message):
    if message.chat.id == config.admin_id_1 or message.chat.id == config.user_schedule1 or message.chat.id == config.user_schedule2:
        loging(logger_level='WARN', user_id=str(message.chat.id), do='Received \'[photo]\'')
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = 'schedule.jpg'
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Start uploading photos . . .')
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        loging(logger_level='INFO', user_id=str(message.chat.id), do='Successfully !')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '✅ Расписание сохранено!')
        status_text(user_id=message.chat.id)
        bot.send_message(message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(message.chat.id), do='Start of the mailing list')
        status_text(user_id=message.chat.id)
        send_message(user_id=message.chat.id, text='⚠ Обновлено расписание.', i=0)

# inline-button
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    loging(logger_level='INFO', user_id=str(call.message.chat.id), do=f'Call \'[{call.data}]\'')
    # Show D/Z
    if call.data == 'russian_lang':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'literature':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'native_literature':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'english_lang_1':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'english_lang_2':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'algebra':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'geometry':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'TBIS':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'computer_science':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'story':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'social_science':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'geography':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'physics':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'chemistry':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'biology':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'music':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'technology':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    elif call.data == 'OBZH':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, str(db.return_dz(user_id=call.message.chat.id, lesson=call.data)[0]))
    # Replace D/Z
    elif call.data == 'russian_lang_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Русский язык].', i=0)
    elif call.data == 'literature_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        loging(logger_level='INFO', user_id=str(call.message.chat.id), do='Successfully !')
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Литература].', i=0)
    elif call.data == 'native_literature_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Родноя литература].', i=0)
    elif call.data == 'english_lang_1_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Иностранный язык (1 группа)].', i=0)
    elif call.data == 'english_lang_2_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Иностранный язык (2 группа)].', i=0)
    elif call.data == 'algebra_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Алгебра].', i=0)
    elif call.data == 'geometry_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Геометрия].', i=0)
    elif call.data == 'TBIS_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Теория вероятностей и статистика].', i=0)
    elif call.data == 'computer_science_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Информатика].', i=0)
    elif call.data == 'story_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [История].', i=0)
    elif call.data == 'social_science_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Обществознание].', i=0)
    elif call.data == 'geography_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [География].', i=0)
    elif call.data == 'physics_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Физика].', i=0)
    elif call.data == 'chemistry_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Химия].', i=0)
    elif call.data == 'biology_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Биология].', i=0)
    elif call.data == 'music_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Музыка].', i=0)
    elif call.data == 'technology_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [Технология].', i=0)
    elif call.data == 'OBZH_update':
        status_text(user_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, '⚙️ Replacement in progress, please wait . . .', reply_markup=types.ReplyKeyboardRemove())
        db.replace_dz(user_id=call.message.chat.id, lesson=call.data.replace("_update", ""), dz=input_dz)
        bot.send_message(call.message.chat.id, '✅ Successfully !')
        bot.send_message(call.message.chat.id, '⚠ Активирована система уведомлений . . .', reply_markup=types.ReplyKeyboardRemove())
        loging(logger_level='WARN', user_id=str(call.message.chat.id), do='Start of the mailing list')
        status_text(user_id=call.message.chat.id)
        send_message(user_id=call.message.chat.id, text='⚠ Обновлено Д/З [ОБЖ].', i=0)

# Text
@bot.message_handler(content_types=['text'])
def logic(message):
    loging(logger_level='INFO', user_id=str(message.chat.id), do=f'Received \'{message.text}\'')
    if message.text == 'Домашнее задание 📚':
        dz(message)
    elif message.text == 'Расписание 📑':
        schedule(message)
    elif message.text == 'Расписание звонков 🕝':
        call_schedule(message)
    # Admin Panel
    elif message.text == f'/{config.commands_admin}':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            status_text(user_id=message.chat.id)
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin logged into the panel . . .')
            bot.send_message(message.chat.id, '''🛠Вы в админ-панели!\nБудте осторожны‼️''', reply_markup=markup_admin_panel)
        else:
            status_text(user_id=message.chat.id)
            loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Рассылка✉️':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
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
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '⚠️ Бот будет перезагружен !\n\nПодождите ~20 секунд.')
            db.db_stop(user_id=message.chat.id)
            sleep(1)
            os.system(config.reboot_command)
        else:
            status_text(user_id=message.chat.id)
            loging(logger_level='WARN', user_id=str(message.chat.id), do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Бэкап базы данных 📑':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
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
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
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
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Generating information about: Compiler')
            Compiler = str(platform.python_compiler())
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
Compiler: {Compiler}
-------------------
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
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3 or message.chat.id == config.user_dz_1 or message.chat.id == config.user_dz_2 or message.chat.id == config.user_dz_3 or message.chat.id == config.user_dz_4:
            loging(logger_level='INFO', user_id=str(message.chat.id), do='Admin or user replase D/Z')
            status_text(user_id=message.chat.id)
            global input_dz
            input_dz = message.text
            bot.send_message(message.chat.id, '👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=markup_dz_update)
        else:
            loging(logger_level='INFO', user_id=str(message.chat.id), do=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')
            status_text(user_id=message.chat.id)
            bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌')


loging(logger_level='INFO', user_id='nope', do='Sending notifications to admins . . .')
sleep(1)

bot.send_message(config.admin_id_1, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
# bot.send_message(config.admin_id_2, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
# bot.send_message(config.admin_id_3, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True, long_polling_timeout=60, logger_level=1, interval=0)  # Запуск бота
