import asyncio


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties


from config import config

import log.colors as colors
from log.logging import logging

import handlers.core as core

import handlers.menu
import handlers.start
import handlers.lessons
import handlers.profile
import handlers.schedule
import handlers.admin_panel
import handlers.update_lesson

import database.requests as rq
import database.models as db_models

from keyboards.other import __BACK_IN_MAIN_MENU__

from utils import NotificationAdmins


async def main() -> None:
    log = logging(Name='MAIN', Color=colors.green)

    bot: Bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ))
    dp: Dispatcher = Dispatcher(storage=MemoryStorage())

    dp.include_router(core.GetRouter())

    log.info(user_id=None, msg='The bot is running !')
    await NotificationAdmins('⚠ Бот запущен! ⚠', bot, InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=60)


if __name__ == '__main__':
    asyncio.run(main())
