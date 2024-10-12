from time import sleep
from shutil import move

import aiogram
import aiogram.utils
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

import bot.config as config
from bot.lessons import Lessons
import bot.database.requests as rq
import bot.logging.colors as colors
from bot.database.models import User
import bot.logging.logging as logging
from bot.handlers.core import GetLessons
from bot.keyboards.other import __BACK_IN_MAIN_MENU__

log = logging.logging(Name='UTILS', Color=colors.blue)
auth_users: list[int] = []


async def rename(user_id: int, file_name_in: str, file_name_out: str) -> None:
    log.info(str(user_id), f'Rename {file_name_in} -> {file_name_out}')
    
    try:
        move(file_name_in, file_name_out)
        log.info(str(user_id), 'Successfully !')

    except Exception as Error:
        log.error(str(user_id), str(Error))


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
                await rq.DeleteUser(user.user_id, await rq.GetUser(user.user_id))

            timer += 1

    log.info(str(user_id), 'Mailing is over')
    await bot.send_message(user_id, '✅ Рассылка закончена!',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
    return


async def SendUpdateLesson(user_id: int, lesson_id: str, bot: aiogram.Bot) -> None:
    await newsletter(user_id=user_id, text=f'⚠ Обновлено Д/З [{await GetLessons().GetName(lesson_id)}]', auto=True, bot=bot)
    return


async def CheckForAdmin(user_id: int) -> bool:
    for admin_id in config.__LIST_ADMIN_ID__:
        if user_id == admin_id:
            log.debug(str(user_id), 'Admin check: success')
            return True

    log.debug(str(user_id), 'Admin check: fail')
    return False


async def CheckAuthUser(message: Message, bot: aiogram.Bot) -> bool:
    for user_id in auth_users:
        if user_id == message.chat.id:
            return True

    if await rq.GetUser(message.chat.id) == AttributeError:
        log.info(str(message.chat.id), 'User unauthenticated !')

        await rq.SetUser(
            user_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name,
        )
        await bot.send_message(message.chat.id, f'❌ Ошибка аутентификации !\n\n ✅ Данные добавлены !\n\nVersion: {config.__VERSION__}',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
        return False
    else:
        auth_users.append(message.chat.id)
        return True


async def NotificationAdmins(text: str, bot: aiogram.Bot, reply_markup: aiogram.types.InlineKeyboardMarkup | None = None) -> None:
    log.info(None, 'Sending notifications to admins')
    
    for admin_id in config.__LIST_ADMIN_ID__:
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
