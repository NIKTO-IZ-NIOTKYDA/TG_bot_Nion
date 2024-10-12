import datetime
from httpx import HTTPStatusError

from webapp.backend.netschoolapi.netschoolapi import NetSchoolAPI_


async def create_client(API: str, requests_timeout: int = 3) -> NetSchoolAPI_:
    # Создаём клиент. Через него мы будем обращаться к API электронного дневника
    return NetSchoolAPI_(API, default_requests_timeout=requests_timeout)


async def login(NSAPI: NetSchoolAPI_, login: str, password: str, school: str) -> types_NSAPI.successfully | ValueError | Exception:
    # Логинимся в "Сетевой город"
    try:
        await NSAPI.login(
            login,
            password,
            school,
        )
    except types_NSAPI.errors.AuthError() | types_NSAPI.errors.SchoolNotFoundError(): raise ValueError
    except Exception as Error: raise Error

    return types_NSAPI.successfully


# Дневник
async def diary(
        NSAPI: NetSchoolAPI_,
        start: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()),
        end: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=7)
            ) -> types_NSAPI.schemas.Diary | str:
    if start > end: raise IndexError('start > end')
    try:
        diary = await NSAPI.diary(start=start, end=end)
    except HTTPStatusError: raise HTTPStatusError(message='Сервис дневника недоступен')

    # Возращяем дневник
    return diary


# Просроченные задания
async def overdue(
        NSAPI: NetSchoolAPI_,
        start: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()),
        end: datetime.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=7),
        ) -> types_NSAPI.schemas.Assignment:
    return NSAPI.overdue(start=start, end=end)


# Прикреплённые файлы
async def attachments(NSAPI: NetSchoolAPI_, Assignment: types_NSAPI.schemas.Assignment) -> list[types_NSAPI.schemas.Attachment]:
    return await NSAPI.attachments(assignment_id=Assignment.id)  # type: ignore[no-any-return]


# Объявления
async def announcements(NSAPI: NetSchoolAPI_) -> list[types_NSAPI.schemas.Announcement]:
    return await NSAPI.announcements()  # type: ignore[no-any-return]


# Информация о школе
async def info_school(NSAPI: NetSchoolAPI_) -> types_NSAPI.schemas.School:
    return await NSAPI.school()


async def logout(NSAPI: NetSchoolAPI_) -> types_NSAPI.successfully:
    # Выходим из сессии
    # Если этого не делать, то при заходе на сайт
    # будет появляться предупреждение о безопасности:
    # "Под вашим логином работает кто-то другой..."
    await NSAPI.logout()
