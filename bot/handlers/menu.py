from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import bot.database.requests as rq
from bot.utils import CheckAuthUser
from bot.handlers.start import start
from bot.keyboards.users import GenStart
from bot.keyboards.users import __HOMEWORK__
from bot.handlers.core import log, GetRouter
from bot.keyboards.other import __BACK_IN_MAIN_MENU__
from bot.config import __VERSION__, __SCHEDULE_PATH_FILE__


router = GetRouter()


@router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), msg=f'Received \'[{callback.data}]\'')

    await state.clear()

    if await CheckAuthUser(callback.message, callback.message.bot):
        try:
            await callback.message.edit_text(f'Добро пожаловать !\n\nVersion: {__VERSION__}', reply_markup=await GenStart(callback.message.chat.id))

            await rq.UpdateUser(
                callback.message.chat.id,
                callback.message.chat.username,
                callback.message.chat.first_name,
                callback.message.chat.last_name,
            )
        except TelegramBadRequest: await start(callback.message)
