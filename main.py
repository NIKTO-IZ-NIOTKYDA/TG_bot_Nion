import os
import sqlite3
from time import sleep
from datetime import datetime

import telebot

import config
from KeyboardsMarkup import *

# Colors
normal = '\x1b[0m'
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
purple = '\x1b[35m'

os.system('clear')  # Clear Konsole
bot = telebot.TeleBot(config.BotToken)

text_start = 'text_start'

def loging(logger_level: str, user_id: str, do: str):
    current_time = datetime.now().strftime('%H:%M:%S')
    if logger_level == 'INFO':
        print('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
    elif logger_level == 'WARN':
        print('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
    elif logger_level == 'ERROR':
        print('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
    else:
        print(red+f'ERROR: Unknown logger_level {logger_level}'+normal)
        bot.send_message(config.admin_id_1, f'ERROR: Unknown logger_level {logger_level}')
        exit(1)


print('[FORMAN]   [ID]             [TIME]    [DO]')
loging(logger_level='INFO', user_id='nope', do='The bot is running . . .')
sleep(1)

def db_error(Error):
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print(Error)  # Вывод к консоль
    bot.reply_to(config.admin_id_1, f'Ошибка подключения к SQLite\nName database = \'{config.name_database}\'')  # Вывод админу
    log_name = f'log_error_connection_sql_database_{current_time}.log'  # имя лог файла
    log = open(str(log_name), 'w')
    log.write(f'Time: {current_time}\n\nERROR: {Error}')
    log.close()
    sleep(1)
    bot.send_message(config.admin_id_1, f'log сохранён в файле {log_name}\nРабота бота преостановлена!\n<u><i>Завершение работы через 10 минут!</i></u>', parse_mode='HTML')
    sleep(5)
    bot.close()
    sleep(600)
    exit(1)


try:
    loging(logger_level='INFO', user_id='none', do='Connecting to db . . .')
    sleep(1)
    conn = sqlite3.connect(config.name_database, check_same_thread=False)
    loging(logger_level='INFO', user_id='none', do='Create a course . . .')
    sleep(1)
    cursor = conn.cursor()
except Exception as Error:
    db_error(Error)

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str,  user_lang: str, user_phone_number: str):
    loging(logger_level='INFO', user_id=f'{user_id}', do='Adding data to db . . .')
    cursor.execute('INSERT OR REPLACE INTO users (user_id, user_name, user_surname, username, user_lang, user_phone_number, user_authentication) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, user_lang, user_phone_number, 1))
    conn.commit()

def db_table_bool_return(user_id: int):
    loging(logger_level='INFO', user_id=f'{user_id}', do='Search by db user_id . . .')
    cursor.execute('SELECT user_authentication FROM users WHERE user_id = ' + str(user_id))
    return str(cursor.fetchone())

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
    elif db_table_bool_return(user_id=message.chat.id) == '(1,)':
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='User (authenticated) pressed \'/start\'')
        status_text(message)
        bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
    else:
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='User (unauthenticated) pressed \'/start\'')
        status_text(message)
        bot.send_message(message.chat.id, 'Add the necessary data for the bot to work properly.\n⚙ Send your phone number to continue.', reply_markup=markup_send_nummer)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'[contact]\'')
        try:
            db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, username=message.from_user.username, user_lang=message.from_user.language_code, user_phone_number=message.contact.phone_number)
            status_text(message)
            bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
        except Exception as Error:
            db_error(Error)

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
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin will reboot the bot . . .')
            loging(logger_level='INFO', user_id=message.chat.id, do='Saving data to db . . .')
            conn.commit()
            loging(logger_level='WARN', user_id=message.chat.id, do='Disconnect from db . . .')
            conn.close()
            loging(logger_level='INFO', user_id=message.chat.id, do='Successfully !')
            loging(logger_level='WARN', user_id=message.chat.id, do='Rebooting . . .')
            sleep(1)
            os.system(config.reboot_command)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Бэкап базы данных 📑':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            with open('sql_damp.txt', 'w') as f:
                for sql in conn.iterdump():
                    f.write(sql)
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
