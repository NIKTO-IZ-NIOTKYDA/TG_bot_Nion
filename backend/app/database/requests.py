from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from database.models import Schedule, log
from database.models import async_session
from database.models import User, Admin, Lesson


async def __SaveData(user_id: int | None, session: AsyncSession) -> None:
    log.debug(user_id=str(user_id), msg='Saving data to db')
              
    await session.flush()
    await session.commit()


async def SyncLessons(lessons: list[list[str]]):
    log.init('Starting sync lessons')

    async with async_session() as session:
        try:
            # Get the list of existing lesson IDs
            c = select(Lesson)
            s = await session.scalars(c)
            existing_lesson: list[Lesson] = s.all()
            existing_lesson_ids: list[str] = []
            
            for lesson in existing_lesson:
                existing_lesson_ids.append(lesson.lesson_id)

            # Create new lesson IDs
            for lesson in lessons:
                if lesson[0] not in existing_lesson_ids:
                    log.init(f'Subject \'{lesson[0]}\' not found in the Lessons table')
                    
                    session.add(Lesson(lesson_id=lesson[0], photo=None))
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
        except Exception as Error:
            log.error(None, str(Error))


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


async def SetAdmin(user_id: int, admin_id: int) -> None | AttributeError | IntegrityError | Exception:
    log.info(user_id=str(user_id), msg=f'Setting admin [{admin_id}]')

    async with async_session() as session:
        try:
            session.add(Admin(
                user_id = admin_id
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
                    photo: bool | None = None,
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


### GETTING


async def GetUser(user_id: int, rq_user_id: int) -> User | AttributeError | Exception:
    log.info(user_id=str(user_id), msg=f'Getting User: \'{rq_user_id}\'')

    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.user_id == rq_user_id))

            if user == None:
                log.warn(user_id, f'User \'{rq_user_id}\' not found!')
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


async def GetAdmin(user_id: int, admin_id: int) -> Admin | AttributeError | Exception:
    log.info(user_id=str(user_id), msg=f'Getting Admin: \'{admin_id}\'')

    async with async_session() as session:
        try:
            user = await session.scalar(select(Admin).where(Admin.user_id == admin_id))

            if user == None:
                log.warn(user_id, f'Admin \'{admin_id}\' not found!')
                return AttributeError
            else: return user
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def GetAdmins(user_id: int) -> list[Admin] | Exception:
    log.info(user_id=str(user_id), msg='Getting Admins . . .')

    async with async_session() as session:
        try:
            return (await session.scalars(select(Admin))).all()
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


async def GetSchedule(user_id: int) -> Schedule | FileNotFoundError | Exception:
    log.info(user_id=str(user_id), msg=f'Getting Schedule: \'{user_id}\'')

    async with async_session() as session:
        try:
            schedule = await session.scalar(select(Schedule).where(Schedule.id == 1))

            if schedule == None or schedule.photo == None:
                log.warn(user_id, f'Schedule not found!')
                return FileNotFoundError
            else: return schedule
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


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


async def UpdateSchedule(user_id: int, photo: bytes | None) -> None | IndentationError | Exception:
    log.info(user_id=str(user_id), msg='Updating User')

    async with async_session() as session:
        try:
            schedule = await session.scalar(select(Schedule).where(Schedule.id == 1))

            if schedule == None:
                log.error(user_id, f'SCHEDULE NOT FOUNT')
                
                session.add(Schedule(
                    id = 1
                ))
                await __SaveData(user_id, session)

                return (await UpdateSchedule(user_id, photo))
                

            schedule.photo = photo

            await __SaveData(user_id, session)
            return

        except IntegrityError as Error:
            log.error(user_id, f'ERROR: {Error.orig} REQUESTS: {Error.statement}')
            return Error
        
        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


### DELETING


async def DeleteUser(user_id: int, user: User) -> None | AttributeError | Exception:
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


async def DeleteAdmin(user_id: int, admin: Admin) -> None | AttributeError | Exception:
    log.warn(user_id, msg=f'Deleting Admin: {admin.user_id}')

    async with async_session() as session:
        try:
            await session.delete(admin)

            await __SaveData(user_id, session)
            return

        except AttributeError as Error:
            log.error(user_id, str(Error))
            return Error

        except Exception as Error:
            log.error(user_id, str(Error))
            return Error
