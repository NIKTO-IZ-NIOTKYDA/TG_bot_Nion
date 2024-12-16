from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from config import config
import database.requests as rq
from utils import CheckAuthUser
from handlers.start import start
from keyboards.users import GenStart
from keyboards.users import __HOMEWORK__
from handlers.core import log, GetRouter
from keyboards.other import __BACK_IN_MAIN_MENU__


router = GetRouter()


@router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), msg=f'Received \'[{callback.data}]\'')

    await state.clear()

    if await CheckAuthUser(callback.message, callback.message.bot):
        try:
            await callback.message.edit_text(f'Добро пожаловать !\n\nRelease: {config.GetRELEASE}', reply_markup=await GenStart(callback.message.chat.id))

            await rq.UpdateUser(
                callback.message.chat.id,
                callback.message.chat.username,
                callback.message.chat.first_name,
                callback.message.chat.last_name,
            )
        except TelegramBadRequest: await start(callback.message)
