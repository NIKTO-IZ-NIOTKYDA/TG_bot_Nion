from enum import IntEnum, unique

from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL_ERROR = 4


def GetLogLevel(log_level: int) -> LogLevel:
    try:
        if int(log_level) == 0: return LogLevel.DEBUG
        elif int(log_level) == 1: return LogLevel.INFO
        elif int(log_level) == 2: return LogLevel.WARN
        elif int(log_level) == 3: return LogLevel.ERROR
        elif int(log_level) == 4: return LogLevel.CRITICAL_ERROR
        else: raise AttributeError
    except ValueError as VE: raise VE


class CONFIG(BaseSettings):
    # Telegram bot
    BOT_TOKEN: str
    TG_USERNAME_DEVELOPER: str

    # Backend
    BACKEND_PORT: int
    LOG_LEVEL: LogLevel
    LOG_FILE_NAME: str
    VERSION_MAJOR: str
    VERSION_MINOR: str
    VERSION_PATCH: str
    VERSION_TYPE: str
    RELEASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_CONTAINER_NAME: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: str
    NO_FOUND_HOMEWORK_MSG: str
    SECRET_KEY: str
    ALGORITHM: str
    SALT512: bytes

    model_config = SettingsConfigDict()
    

    def GetRelease(self):
        return (f'Release {self.VERSION_MAJOR}.{self.VERSION_MINOR}.{self.VERSION_PATCH} [{self.VERSION_TYPE}]')


config = CONFIG()
