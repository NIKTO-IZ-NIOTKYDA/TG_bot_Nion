import asyncio


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties


from bot.config import __BOT_TOKEN__

import bot.logging.colors as colors
from bot.logging.logging import logging

import bot.handlers.core as core

import bot.handlers.start
import bot.handlers.menu
import bot.handlers.lessons
import bot.handlers.schedule
import bot.handlers.profile
import bot.handlers.admin_panel
import bot.handlers.update_lesson

import bot.database.requests as rq
import bot.database.models as db_models

from bot.keyboards.other import __BACK_IN_MAIN_MENU__

from bot.utils import NotificationAdmins


async def main() -> None:
    await db_models.init_db()
    await rq.SyncLessons(core.GetLessons().lessons)

    log = logging(Name='MAIN', Color=colors.green)

    bot: Bot = Bot(__BOT_TOKEN__, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ))
    dp: Dispatcher = Dispatcher(storage=MemoryStorage())

    dp.include_router(core.GetRouter())

    log.info(user_id=None, msg='The bot is running !')
    await NotificationAdmins('⚠Бот запущен!⚠', bot, InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=60)


if __name__ == '__main__':
    asyncio.run(main())
