from os import system
from sys import stdout
from time import sleep
from datetime import datetime

from config import ClearKonsole, log, debug, welcome_animation, name_log_file


# Colors
normal = '\x1b[0m'
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
purple = '\x1b[35m'

log_file = open(str(name_log_file), 'w+')

def welcome_ani():
    system(ClearKonsole)
    load_str = 'launching a telegram bot...'
    ls_len = len(load_str)
    animation = "|/-\\"
    anicount = 0
    counttime = 0
    i = 0
    while counttime != 100:
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
        stdout.write("\r"+res + animation[anicount])
        stdout.flush()
        load_str = res
        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1


if welcome_animation:
    welcome_ani()
if debug:
    print('\n[FORMAN]   [ID]             [TIME]    [DO]')
log_file.write('[FORMAN]   [ID]             [TIME]    [DO]\n')

def loging(logger_level: str, user_id: str, do: str):
    if log:
        current_time = datetime.now().strftime('%H:%M:%S')
        if logger_level == 'INFO':
            print('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
            log_file.write('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}\n'))
            log_file.flush()
        elif logger_level == 'WARN':
            print('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
            log_file.write('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}\n'))
            log_file.flush()
        elif logger_level == 'ERROR':
            print('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
            log_file.write('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}\n'))
            log_file.flush()
            exit(1)
