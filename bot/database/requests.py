from base64 import b64encode, b64decode

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.database.encryption import encrypt, decrypt

from bot.database.models import log
from bot.database.models import async_session
from bot.database.models import User, Lesson, NetSchool
from bot.config import __DATABASE__, __NO_FOUND_HOMEWORK_MSG__


async def __SaveData(user_id: int | None, session: AsyncSession) -> None:
    log.debug(user_id=str(user_id), msg='Saving data to db')
              
    await session.flush()
    await session.commit()


async def SyncLessons(lessons: list[list[str]]):
    log.init('Starting sync lessons')

    async with async_session() as session:
        # Get the list of existing lesson IDs
        existing_lesson_ids: list[str] = (await session.scalars(select(Lesson.lesson_id))).fetchall()

        # Create new lesson IDs
        for lesson in lessons:
            if lesson[0] not in existing_lesson_ids:
                log.init(f'Subject \'{lesson[0]}\' not found in the Lessons table')
                session.add(Lesson(lesson_id=lesson[0], photo=False))
                log.init(f'Subject \'{lesson[0]}\' added in the Lessons table')

        # Delete lessons that are not in the provided list
        for lesson_id in existing_lesson_ids:
            deleting = True

            for lesson in lessons:
                if lesson_id == lesson[0]: deleting = False

            if deleting:
                await session.delete(await session.scalar(select(Lesson).where(Lesson.lesson_id == lesson_id)))

                log.init(f'The field \'{lesson_id}\' from the Lessons table is removed')

        # Save the changes
        await __SaveData(None, session)


### SETTING


async def SetUser(user_id: int, username: str, first_name: str, last_name: str) -> None | IntegrityError | Exception:
    log.info(user_id=str(user_id), msg='Setting User')

    async with async_session() as session:
        try:
            session.add(User(
                user_id = user_id,
                username = username,
                first_name = first_name,
                last_name = last_name,
                send_notifications = True
            ))

            await __SaveData(user_id, session)
            return

        except IntegrityError as Error:
            log.error(user_id, f'ERROR: {Error.orig} REQUESTS: {Error.statement}')
            return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def SetLesson(user_id: int,
                    lesson_id: str,
                    homework: str | None = None,
                    photo: bool = False,
                    url: str | None = None
                    ) -> None | AttributeError | Exception:
    log.info(str(user_id), f'Setting Lesson: \'{lesson_id}\' / homework: \'{homework}\' / photo: \'{photo}\' / url: \'{url}\'')

    async with async_session() as session:
        try:
            lesson: Lesson = await session.scalar(select(Lesson).where(Lesson.lesson_id == lesson_id))

            lesson.homework = homework
            lesson.photo = photo
            lesson.url = url

            await __SaveData(user_id, session)
            return

        except AttributeError as Error:
            log.error(user_id, str(Error))
            return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def SetSendNotifications(user_id: int, send_notifications: bool) -> None | AttributeError | Exception:
    log.info(str(user_id), f'Setting SendNotifications \'{send_notifications}\'')

    async with async_session() as session:
        try:
            (await session.scalar(select(User).where(User.user_id == user_id))).send_notifications = send_notifications
            
            await __SaveData(user_id, session)
            return

        except AttributeError as Error:
            log.error(user_id, str(Error))
            return Error
                
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def SetNetSchool(user_id: int, login: str, password: str, key: str) -> None | AttributeError | IntegrityError | Exception:
    log.info(str(user_id), 'Encrypting login and password')

    b64_login = b64encode(login.encode('utf-8'))
    aes256_password = await encrypt(password, key)
    b64_key = b64encode(key.encode('utf-8'))

    log.info(str(user_id), f'Setting NetSchool')

    async with async_session() as session:
        try:
            session.add(NetSchool(
                user_id = user_id,
                enc_login = b64_login,
                enc_password = aes256_password,
                enc_key = b64_key
            ))
            
            await __SaveData(user_id, session)
            return

        except AttributeError as Error:
                log.error(user_id, str(Error))
                return Error

        except IntegrityError as Error:
            log.error(user_id, f'ERROR: {Error.orig} REQUESTS: {Error.statement}')
            return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


### GETTING


async def GetUser(user_id: int) -> User | AttributeError | Exception:
    log.info(user_id=str(user_id), msg=f'Getting User: \'{user_id}\'')

    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.user_id == user_id))

            if user == None:
                log.warn(user_id, f'User \'{user_id}\' not found!')
                return AttributeError
            else: return user
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def GetUsers(user_id: int) -> list[User] | Exception:
    log.info(user_id=str(user_id), msg='Getting Users . . .')

    async with async_session() as session:
        try:
            return (await session.scalars(select(User))).all()

        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def GetLesson(user_id: int, lesson_id: str) -> Lesson | AttributeError | Exception:
    log.info(user_id, f'Getting Lesson: \'{lesson_id}\'')

    async with async_session() as session:
        try:
            return (await session.scalar(select(Lesson).where(Lesson.lesson_id == lesson_id)))

        except AttributeError as Error:
                log.error(user_id, str(Error))
                return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def GetLessons(user_id: int) -> list[Lesson] | AttributeError | Exception:
    log.info(user_id, f'Getting Lessons')

    async with async_session() as session:
        try:
            return (await session.scalars(select(Lesson))).all()

        except AttributeError as Error:
                log.error(user_id, str(Error))
                return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def GetNetSchool(user_id: int, decode: bool = True) -> NetSchool | bool | AttributeError | Exception:
    log.info(str(user_id), 'Getting NetSchool')

    async with async_session() as session:
        try:
            result = await session.scalar(select(NetSchool).where(NetSchool.user_id == user_id))
        
        except AttributeError as Error:
            log.error(user_id, str(Error))
            return Error

    if not decode and result != None: return True
    elif not decode and result == None: return False

    if decode and result != None:
        try:
            result.enc_login = b64decode(result.enc_login).decode('utf-8')
            result.enc_key = b64decode(result.enc_key).decode('utf-8')
            result.enc_password = await decrypt(encrypted_password=result.enc_password, key=result.enc_key)

            return result

        except Exception as Error:
            log.info(str(user_id), 'Incorrect key')
            return Error
    else:
        log.warn(user_id, f'NetSchool not found!')
        return AttributeError


### Updating


async def UpdateUser(user_id: int, username: str, first_name: str, last_name: str) -> None | IndexError | IntegrityError | Exception:
    log.info(user_id=str(user_id), msg='Updating User')

    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.user_id == user_id))

            if user == None:
                log.error(user_id, f'USER: {user_id} NOT FOUNT')
                return IndexError

            user.username = username
            user.first_name = first_name
            user.last_name = last_name

            await __SaveData(user_id, session)
            return

        except IntegrityError as Error:
            log.error(user_id, f'ERROR: {Error.orig} REQUESTS: {Error.statement}')
            return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


### DELETING


async def DeleteUser(user_id, user: User) -> None | AttributeError | Exception:
    log.warn(user_id, msg=f'Deleting User: {user.user_id}')

    async with async_session() as session:
        try:
            await session.delete(user)

            await __SaveData(user_id, session)
            return

        except AttributeError as Error:
            log.error(user_id, str(Error))
            return Error

        except Exception as Error:
            log.error(user_id, str(Error))
            return Error
