from datetime import datetime

from config import log, debug, name_log_file, main_admin_id


# Colors
normal = '\x1b[0m'
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
purple = '\x1b[35m'

log_file = open(str(name_log_file), 'w+')
if debug:
    print('[FORMAN]   [ID]             [TIME]    [DO]')
log_file.write('[FORMAN]   [ID]             [TIME]    [DO]\n')

def loging(logger_level: str, user_id: str, do: str):
    if log:
        if user_id == str(main_admin_id+1):
            pass
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            if logger_level == 'INFO':
                if debug:
                    print('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}\n'))
                log_file.flush()
            elif logger_level == 'WARN':
                if debug:
                    print('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}\n'))
                log_file.flush()
            elif logger_level == 'ERROR':
                if debug:
                    print('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}\n'))
                log_file.flush()
                exit(1)
