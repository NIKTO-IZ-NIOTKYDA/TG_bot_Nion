import os
from time import sleep

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

def status_text(message):
    loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Send status . . .')
    bot.send_chat_action(message.chat.id, action='typing')


@bot.message_handler(commands=['start'])
def start(message):
    loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'/start\'')
    if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
        status_text(message)
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Admin pressed \'/start\'')
        bot.send_message(message.chat.id, f'Для доступа к админ панели введите: \n/{config.commands_admin}')
        bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
    elif db.db_table_bool_return(user_id=message.chat.id) == '(1,)':
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='User (authenticated) pressed \'/start\'')
        status_text(message)
        bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
    else:
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='User (unauthenticated) pressed \'/start\'')
        status_text(message)
        bot.send_message(message.chat.id, 'Add the necessary data for the bot to work properly.\n⚙ Send your phone number to continue.', reply_markup=markup_send_nummer)


@bot.message_handler(commands=['update_date_db'])
def update_date_db(message):
    loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'/update_date_db\'')
    status_text(message)
    bot.send_message(message.chat.id, '⚙ Send your phone number to continue.', reply_markup=markup_send_nummer)

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'[contact]\'')
        db.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, username=message.from_user.username, user_lang=message.from_user.language_code, user_phone_number=message.contact.phone_number)
        status_text(message)
        bot.send_message(message.chat.id, '✅ Data has been successfully added/updated in the database')
        status_text(message)
        bot.send_message(message.chat.id, text_start, reply_markup=markup_start)

@bot.message_handler(content_types=['text'])
def logic(message):
    if message.text == '':
        status_text(message)
        bot.send_message(message.chat.id, '')
    elif message.text == '':
        status_text(message)
        bot.send_message(message.chat.id, '')
    elif message.text == '':
        status_text(message)
        bot.send_message(message.chat.id, '')
        # Admin Panel
    elif message.text == f'/{config.commands_admin}':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            status_text(message)
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin logged into the panel . . .')
            bot.send_message(message.chat.id, '''🛠Вы в админ-панели!\nБудте осторожны‼️''', reply_markup=markup_admin_panel)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Перезагрузка 🔄':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            status_text(message)
            bot.send_message(message.chat.id, '⚠️ Бот будет перезагружен !\n\nПодождите ~20 секунд.')
            db.db_stop(user_id=str(message.chat.id))
            sleep(1)
            os.system(config.reboot_command)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Бэкап базы данных 📑':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            db.db_backup()
            status_text(message)
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin performs db backup . . .')
            bot.send_message(message.chat.id, '✅Бэкап базы данных готов!\nОтправляю . . .')
            loging(logger_level='WARN', user_id=message.chat.id, do='The backup copy of the database is ready, I’m sending it. . .')
            bot.send_chat_action(message.chat.id, 'upload_document')
            bot.send_document(message.chat.id, document=open('sql_damp.txt', 'rb'))
            sleep(1)
            loging(logger_level='WARN', user_id=message.chat.id, do='Deleting a database backup . . .')
            os.system('rm sql_damp.txt')
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Статус сервера 🛠️':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            loging(logger_level='INFO', user_id=message.chat.id, do='Аdmin requested a server status report, generation . . .')
            status_text(message)
            import platform
            import psutil
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: SystemName')
            SystemName = str(platform.system())
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: SystemRelease')
            SystemRelease = str(platform.release())
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: PythonVersion')
            PythonVersion = str(platform.python_version())
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Compiler')
            Compiler = str(platform.python_compiler())
            # Загруженость
            # CPU
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: CPU, CPU_stats')
            cpu = psutil.cpu_times()
            cpu_stats = psutil.cpu_stats()
            # Memory
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Memory_Virtual, Memory_Swap')
            Memory_Virtual = psutil.virtual_memory()
            Memory_Swap = psutil.swap_memory()
            # Disks
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Disks')
            Disks = psutil.disk_io_counters()
            # Network
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Network')
            Network = psutil.net_if_addrs()
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating a report based on the data received . . .')
            info = f'''OS: {SystemName} {SystemRelease}
Python: {PythonVersion} Version
Server: {Compiler}
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
            loging(logger_level='INFO', user_id=message.chat.id, do='Successfully !')
            status_text(message)
            loging(logger_level='INFO', user_id=message.chat.id, do='Report Sent !')
            bot.send_message(message.chat.id, info)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    else:
        status_text(message)
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')
        bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌')


loging(logger_level='INFO', user_id='nope', do='Sending notifications to admins . . .')
sleep(1)

bot.send_message(config.admin_id_1, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
# bot.send_message(config.admin_id_2, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
# bot.send_message(config.admin_id_3, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True, long_polling_timeout=60, logger_level=1, interval=0)  # Запуск бота
