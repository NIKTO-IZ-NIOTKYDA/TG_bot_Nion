import datetime
from datetime import datetime

from config import config
from log.colors import normal, red, green, yellow, blue, purple


log_file = open(config.LOG_FILE_NAME, 'w+')


print('[FORMAT]   [ID]            [TIME]              [MODULE]   [MESSAGE]')
log_file.write('[FORMAT]   [ID]            [TIME]              [MODULE]   [MESSAGE]\n')


class logging:

    def __init__(self, Name: str, Color: str) -> None:
        self.Name = Name
        self.Color = Color

    def init(self, msg: str):
        if config.LOG_LEVEL.value == 0:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (purple+'[INIT]', purple+f'None', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (purple+'[INIT]', purple+f'None', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}\n'))
            log_file.flush()

    def debug(self, user_id: str | None, msg: str) -> None:
        if config.LOG_LEVEL.value == 0:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (blue+'[DEBUG]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (blue+'[DEBUG]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}\n'))
            log_file.flush()

    def info(self, user_id: str | None, msg: str) -> None:
        if config.LOG_LEVEL.value <= 1:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (green+'[INFO]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (green+'[INFO]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}\n'))
            log_file.flush()

    def warn(self, user_id: str | None, msg: str) -> None:
        if config.LOG_LEVEL.value <= 2:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (yellow+'[WARN]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (yellow+'[WARN]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}\n'))
            log_file.flush()

    def error(self, user_id: str | None, msg: str) -> None:
        if config.LOG_LEVEL.value <= 3:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (red+'[ERROR]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (red+'[ERROR]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}\n'))
            log_file.flush()

    def cerror(self, user_id: str | None, msg: str) -> None:
        if config.LOG_LEVEL.value <= 4:
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print('%-15s %-20s %-15s %-15s %-10s' % (red+'[CERROR]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}'))
            log_file.write('%-15s %-20s %-15s %-15s %-10s' % (red+'[CERROR]', purple+f'{user_id}', blue+f'{current_time}', self.Color+f'[{self.Name}]', normal+f'{msg}\n'))
            log_file.flush()
