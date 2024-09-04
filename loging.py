from sys import stdout
from time import sleep
from os import remove, system
from datetime import datetime

import colors_log
from config import clear_konsole, log, debug, name_log_file, welcome_animation

try:
    remove(str(name_log_file))
except FileNotFoundError:
    pass
log_file = open(str(name_log_file), 'w+')


def welcome_ani() -> None:
    system(clear_konsole)
    load_str = 'Launching a telegram bot...'
    ls_len = len(load_str)
    animation = '|/-\\'
    anicount = 0
    counttime = 0
    i = 0
    while counttime != 52:
        sleep(0.075)
        load_str_list = list(load_str)
        x = ord(load_str_list[i])
        y = 0
        if x != 32 and x != 46:
            if x > 90:
                y = x - 32
            else:
                y = x + 32
            load_str_list[i] = chr(y)
        res = ''
        for j in range(ls_len):
            res = res + load_str_list[j]
        stdout.write('\r'+res + animation[anicount])
        stdout.flush()
        load_str = res
        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1


system(clear_konsole)

if welcome_animation:
    welcome_ani()
    system(clear_konsole)

print('[FORMAT]   [ID]            [TIME]              [MODULE]   [MESSAGE]')
log_file.write('[FORMAT]   [ID]            [TIME]              [MODULE]   [MESSAGE]\n')


class logging:

    def __init__(self, Name: str, Color: str) -> None:
        self.Name = Name
        self.Color = Color

    def debug(self, user_id: str | None, msg: str) -> None:
        if log | debug:
            current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.blue+'[DEBUG]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.blue+'[DEBUG]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}\n'))
            log_file.flush()

    def info(self, user_id: str | None, msg: str) -> None:
        if log:
            current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.green+'[INFO]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.green+'[INFO]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}\n'))
            log_file.flush()

    def warn(self, user_id: str | None, msg: str) -> None:
        if log:
            current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.yellow+'[WARN]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.yellow+'[WARN]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}\n'))
            log_file.flush()

    def error(self, user_id: str | None, msg: str) -> None:
        if log:
            current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+'[ERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+'[ERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}\n'))
            log_file.flush()

    def cerror(self, user_id: str | None, msg: str) -> None:
        if log:
            current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+'[CERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+'[CERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{msg}\n'))
            log_file.flush()
