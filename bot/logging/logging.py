import datetime
from os import mkdir
from shutil import move
from os.path import getctime
from datetime import datetime

import bot.logging.colors as colors
from bot.config import __LOGING__, __DEBUGGING__, __LOG_FILE_NAME__

try:
    try: mkdir('logs')
    except FileExistsError: pass

    move(__LOG_FILE_NAME__, f'logs/log_{datetime.fromtimestamp(getctime(__LOG_FILE_NAME__)).strftime('%d.%m.%Y_%H:%M:%S')}.log')
except FileNotFoundError: pass

log_file = open(__LOG_FILE_NAME__, 'w+')


print('[FORMAT]   [ID]            [TIME]              [MODULE]   [MESSAGE]')
log_file.write('[FORMAT]   [ID]            [TIME]              [MODULE]   [MESSAGE]\n')


class logging:

    def __init__(self, Name: str, Color: str) -> None:
        self.Name = Name
        self.Color = Color

    def init(self, msg: str):
        if __LOGING__ | __DEBUGGING__:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors.purple+'[INIT]', colors.purple+f'None', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors.purple+'[INIT]', colors.purple+f'None', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}\n'))
            log_file.flush()

    def debug(self, user_id: str | None, msg: str) -> None:
        if __LOGING__ | __DEBUGGING__:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors.blue+'[DEBUG]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors.blue+'[DEBUG]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}\n'))
            log_file.flush()

    def info(self, user_id: str | None, msg: str) -> None:
        if __LOGING__:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors.green+'[INFO]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors.green+'[INFO]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}\n'))
            log_file.flush()

    def warn(self, user_id: str | None, msg: str) -> None:
        if __LOGING__:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors.yellow+'[WARN]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors.yellow+'[WARN]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}\n'))
            log_file.flush()

    def error(self, user_id: str | None, msg: str) -> None:
        if __LOGING__:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors.red+'[ERROR]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors.red+'[ERROR]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}\n'))
            log_file.flush()

    def cerror(self, user_id: str | None, msg: str) -> None:
        if __LOGING__:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors.red+'[CERROR]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors.red+'[CERROR]', colors.purple+f'{user_id}', colors.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors.normal+f'{msg}\n'))
            log_file.flush()
