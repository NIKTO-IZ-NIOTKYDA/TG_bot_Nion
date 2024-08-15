import asyncio
import datetime
from httpx import HTTPStatusError
from netschoolapi import NetSchoolAPI


async def create_client(API: str) -> NetSchoolAPI:
    # Создаём клиент. Через него мы будем обращаться к API электронного дневника
    return NetSchoolAPI(API)


async def login(ns: NetSchoolAPI, login: str, password: str, school: str) -> None | Exception:
    # Логинимся в "Сетевой город"
    try:
        await ns.login(
            login,
            password,
            school,
        )
    except Exception as Error:
        return Error

    return None


async def diary(ns: NetSchoolAPI) -> list[list[datetime.date | int | str]] | str:
    # Печатаем дневник на текущую неделю
    # О полях дневника в "Справочнике"
    try:
        print(await ns.diary())
    except HTTPStatusError:
        return 'Сервис дневника недоступен. Ошибка подключения.'

    return [[datetime.date.today(), 0, '0']]


async def logout(ns: NetSchoolAPI) -> None:
    # Выходим из сессии
    # Если этого не делать, то при заходе на сайт
    # будет появляться предупреждение о безопасности:
    # "Под вашим логином работает кто-то другой..."
    await ns.logout()


asyncio.run(create_client(API='0'))
