from datetime import datetime

from config import log, main_admin_id

# Colors
normal = '\x1b[0m'
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
purple = '\x1b[35m'


def loging(logger_level: str, user_id: str, do: str):
    if log:
        if user_id == str(main_admin_id):
            pass
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            if logger_level == 'INFO':
                print('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
            elif logger_level == 'WARN':
                print('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
            elif logger_level == 'ERROR':
                print('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
            else:
                print(red+f'ERROR: Unknown logger_level {logger_level}'+normal)
                exit(1)
