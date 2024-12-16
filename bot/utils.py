from time import sleep

import aiogram
import aiogram.utils
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from config import config
import log.colors as colors
import log.logging as logging
import database.requests as rq
from handlers.core import GetLessons
from database.models import Admin, User
from keyboards.other import __BACK_IN_MAIN_MENU__


log = logging.logging(Name='UTILS', Color=colors.blue)
auth_users: list[int] = []
LIST_ADMIN_ID: list[int] = []


async def GetAdminsID(user_id: int) -> list[int] | Exception:
    if LIST_ADMIN_ID != []: return LIST_ADMIN_ID
    else:
        try:
            admins: list[Admin] = await rq.GetAdmins(user_id)

            for admin in admins:
                LIST_ADMIN_ID.append(admin.user_id)
            
            return LIST_ADMIN_ID

        except Exception as Error:
            log.error(user_id, str(Error))
            return Error


async def GetTimeToLesson(lessons: list[dict[str, str]], current_time: str) -> tuple[int, float] | tuple[int, None]:
    current_hour, current_minute = map(float, str(current_time).split('.'))
    current_time_in_minutes = current_hour * 60 + current_minute
    
    for i, lesson in enumerate(lessons):
        start_time = sum(float(x) * 60**i for i, x in enumerate(reversed(str(lesson['start_time']).split('.'))))
        end_time = sum(float(x) * 60**i for i, x in enumerate(reversed(str(lesson['end_time']).split('.'))))
        
        if start_time <= current_time_in_minutes <= end_time:
            return 0, end_time - current_time_in_minutes
        
        if i < len(lessons) - 1:
            next_start_time = sum(float(x) * 60**i for i, x in enumerate(reversed(lessons[i+1]['start_time'].split('.'))))
            if end_time < current_time_in_minutes < next_start_time:
                return 1, next_start_time - current_time_in_minutes
    
    return -1, None


async def newsletter(user_id: int, text: str, auto: bool, bot: aiogram.Bot) -> None:
    log.warn(user_id=str(user_id), msg='Start of the mailing')

    users: list[User] = await rq.GetUsers(user_id)

    if users != None:
        timer: int = 0

        for user in users:
            if timer == 29:
                timer = 0
                sleep(1.15)

            try:
                if (user.send_notifications and auto) or not auto:
                    await bot.send_message(chat_id=user.user_id, text=text,
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
                    log.info(str(user.user_id), f'Sent: {user.user_id}')

            except TelegramBadRequest:
                log.warn(str(user.user_id), f'User {user.user_id} has blocked the bot!')
                # TODO: MARK: DELETE
                #await rq.DeleteUser(user.user_id, await rq.GetUser(user.user_id, user.user_id))

            timer += 1

    log.info(str(user_id), 'Mailing is over')
    await bot.send_message(user_id, '✅ Рассылка закончена!',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
    return


async def SendUpdateLesson(user_id: int, lesson_id: str, bot: aiogram.Bot) -> None:
    await newsletter(user_id=user_id, text=f'⚠ Обновлено Д/З [{await GetLessons().GetName(lesson_id)}]', auto=True, bot=bot)
    return


async def CheckForAdmin(user_id: int) -> bool:
    for admin_id in await GetAdminsID(user_id):
        if user_id == admin_id:
            log.debug(str(user_id), 'Admin check: success')
            return True

    log.debug(str(user_id), 'Admin check: fail')
    return False


async def CheckAuthUser(message: Message, bot: aiogram.Bot) -> bool:
    for user_id in auth_users:
        if user_id == message.chat.id:
            return True

    if await rq.GetUser(message.chat.id, message.chat.id) == AttributeError:
        log.info(str(message.chat.id), 'User unauthenticated !')

        await rq.SetUser(
            user_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name,
        )
        await bot.send_message(message.chat.id, f'❌ Ошибка аутентификации !\n\n ✅ Данные добавлены !\n\nVersion: {config.GetRELEASE}',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
        return False
    else:
        auth_users.append(message.chat.id)
        return True


async def NotificationAdmins(text: str, bot: aiogram.Bot, reply_markup: aiogram.types.InlineKeyboardMarkup | None = None) -> None:
    log.info(None, 'Sending notifications to admins')
    admins_id = await GetAdminsID(config.ROOT_ID)

    for admin_id in admins_id:
        try:
            await bot.send_message(chat_id=admin_id, text=text, reply_markup=reply_markup)
            log.info(None, f'Send {admin_id}')
        except TelegramBadRequest:
            log.warn(str(admin_id), f'Admin {admin_id} blocked or didn\'t start the bot!')


async def RQReporter(callback: CallbackQuery):
    await callback.answer(f'❌ Запрос не удался!\n\nLOG:\ncallback.data: \'{callback.data}\'', show_alert=True)


def format_date(date):
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    
    day_of_week = days_of_week[date.weekday()]
    day = date.day
    month = months[date.month - 1]
    year = date.year
    
    return f'{day_of_week}, {day} {month} {year} г.'


# async def sync_database(user_id: int, SessionNetSchool: NetSchoolAPI):
#     log.info(user_id, 'Started DB synchronization')
#     try:
#         init_filters = await SessionNetSchool.initfilters(class_data=await SessionNetSchool.params_average_mark(), json = True)

#         dairy = await SessionNetSchool.diary(
#             start=init_filters['start'],
#             end=init_filters['end'],
#             json=True
#         )
#         log.debug(user_id, f'{dairy}')

#         for day in dairy['weekDays']:
#             log.debug(user_id, f'{day}')
#             for lesson in day['lessons']:
#                 log.debug(user_id, f'{lesson}')
#                 for assignment in lesson['assignments']:
#                     log.debug(user_id, f'{assignment}')
#                     if assignment['mark'] != None:
#                         # TODO: Check была ли оценка

#                         data = await SessionNetSchool.diary_assigns(assignment['mark']['assignmentId'])
#                         log.debug(user_id, f'{data}')
                            
        
#         await rq.SetNetSchoolData(user_id, dairy)
#     except Exception:
#         import traceback
#         print(traceback.format_exc())
