from os import remove, system
from datetime import datetime

import colors_log
from config import clear_konsole, log, debug, name_log_file

try:
    remove(str(name_log_file))
except FileNotFoundError:
    pass
log_file = open(str(name_log_file), 'w+')

system(clear_konsole)
print('[FORMAT]   [ID]            [TIME]              [MODULE]   [DO]')
log_file.write('[FORMAT]   [ID]            [TIME]              [MODULE]   [DO]\n')
class logging:
    current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    def __init__(self, Name: str, Color: str) -> None:
         self.Name = Name
         self.Color = Color

    def debug(self, user_id: str | None, do: str):
            if log and debug:
                print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.blue+f'[DEBUG]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.blue+f'[DEBUG]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}\n'))
                log_file.flush()
    def info(self, user_id: str | None, do: str):
            if log:
                print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.green+f'[INFO]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.green+f'[INFO]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}\n'))
                log_file.flush()
    def warn(self, user_id: str | None, do: str):
         if log:
                print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.yellow+f'[WARN]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.yellow+f'[WARN]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}\n'))
                log_file.flush()
    def error(self, user_id: str | None, do: str):
            if log:
                print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+f'[ERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+f'[ERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}\n'))
                log_file.flush()
    def cerror(self, user_id: str | None, do: str):
            if log:
                print('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+f'[CERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}'))
                log_file.write('%-15s %-20s %-15s %-15s %-10s' % (colors_log.red+f'[CERROR]', colors_log.purple+f'{user_id}', colors_log.blue+f'{self.current_time}', self.Color+f'[{self.Name}]', colors_log.normal+f'{do}\n'))
                log_file.flush()
                exit(1)
