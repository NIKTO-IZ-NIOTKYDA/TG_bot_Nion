import datetime
from httpx import HTTPStatusError

import webapp.backend.netschoolapi.errors as errors
import webapp.backend.netschoolapi.schemas as schemas
from webapp.backend.netschoolapi.netschoolapi import NetSchoolAPI_


async def create_client(API: str, requests_timeout: int = 3) -> NetSchoolAPI_:
    # Создаём клиент. Через него мы будем обращаться к API электронного дневника
    return NetSchoolAPI_(API, default_requests_timeout=requests_timeout)


async def login(NSAPI: NetSchoolAPI_, login: str, password: str, school: str) -> None | ValueError | Exception:
    # Логинимся в "Сетевой город"
    try:
        await NSAPI.login(
            login,
            password,
            school,
        )
    except errors.AuthError() | errors.SchoolNotFoundError(): raise ValueError
    except Exception as Error: raise Error


# Дневник
async def diary(
        NSAPI: NetSchoolAPI_,
        start: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()),
        end: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=7)
            ) -> schemas.Diary | dict:
    if start > end: raise IndexError('start > end')
    try:
        diary = await NSAPI.diary(start=start, end=end, json=True)
    except HTTPStatusError: raise HTTPStatusError(message='Сервис дневника недоступен')

    return diary


# Просроченные задания
async def overdue(
        NSAPI: NetSchoolAPI_,
        start: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()),
        end: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=7),
        ) -> dict:
    return NSAPI.overdue(start=start, end=end, json=True)


# Прикреплённые файлы
async def attachments(NSAPI: NetSchoolAPI_, Assignment: schemas.Assignment) -> dict:
    return await NSAPI.attachments(assignment_id=Assignment.id, json=True)  # type: ignore[no-any-return]


# Объявления
async def announcements(NSAPI: NetSchoolAPI_) -> dict:
    return await NSAPI.announcements(json=True)  # type: ignore[no-any-return]


# Информация о школе
async def info_school(NSAPI: NetSchoolAPI_) -> dict:
    return await NSAPI.school()


async def logout(NSAPI: NetSchoolAPI_) -> None:
    # Выходим из сессии
    # Если этого не делать, то при заходе на сайт
    # будет появляться предупреждение о безопасности:
    # "Под вашим логином работает кто-то другой..."
    await NSAPI.logout()
