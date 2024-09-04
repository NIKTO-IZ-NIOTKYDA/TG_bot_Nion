import datetime
from httpx import HTTPStatusError

import sgo.types_NSAPI as types_NSAPI
from netschoolapi import NetSchoolAPI


async def create_client(API: str, requests_timeout: int = 3) -> NetSchoolAPI:
    # Создаём клиент. Через него мы будем обращаться к API электронного дневника
    return NetSchoolAPI(API, default_requests_timeout=requests_timeout)


async def login(NSAPI: NetSchoolAPI, login: str, password: str, school: str) -> types_NSAPI.successfully | ValueError | Exception:
    # Логинимся в "Сетевой город"
    try:
        await NSAPI.login(
            login,
            password,
            school,
        )
    except types_NSAPI.errors.AuthError() | types_NSAPI.errors.SchoolNotFoundError():
        return ValueError

    except Exception as Error:
        return Error

    return types_NSAPI.successfully


# Дневник
async def diary(
        NSAPI: NetSchoolAPI,
        start: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()),
        end: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=7)
                ) -> types_NSAPI.schemas.Diary | str:
    # Проверяем начало выбоки > конец
    if start > end:
        return 'start > end'
    try:
        diary = await NSAPI.diary(start=start, end=end)
    except HTTPStatusError:
        return 'Сервис дневника недоступен. Ошибка подключения.'

    # Возращяем дневник на текущую неделю
    return diary


# Просроченные задания
async def overdue(
        NSAPI: NetSchoolAPI,
        start: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()),
        end: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=7),
        ) -> types_NSAPI.schemas.Assignment:
    return NSAPI.overdue(start=start, end=end)


# Прикреплённые файлы
async def attachments(NSAPI: NetSchoolAPI, Assignment: types_NSAPI.schemas.Assignment) -> list[types_NSAPI.schemas.Attachment]:
    return await NSAPI.attachments(assignment_id=Assignment.id)  # type: ignore[no-any-return]


# Объявления
async def announcements(NSAPI: NetSchoolAPI) -> list[types_NSAPI.schemas.Announcement]:
    return await NSAPI.announcements()  # type: ignore[no-any-return]


# Информация о школе
async def info_school(NSAPI: NetSchoolAPI) -> types_NSAPI.schemas.School:
    return await NSAPI.school()


async def logout(NSAPI: NetSchoolAPI) -> types_NSAPI.successfully:
    # Выходим из сессии
    # Если этого не делать, то при заходе на сайт
    # будет появляться предупреждение о безопасности:
    # "Под вашим логином работает кто-то другой..."
    await NSAPI.logout()
