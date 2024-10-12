from aiogram.types import Message
from aiogram.filters import Command

from bot.config import __VERSION__
import bot.database.requests as rq
from bot.utils import CheckAuthUser
from bot.keyboards.users import GenStart
from bot.handlers.core import log, GetRouter


router = GetRouter()


@router.message(Command('start'))
async def start(message: Message) -> None:
    log.info(str(message.chat.id), 'Received \'/start\'')

    if not await CheckAuthUser(message, message.bot):
        await rq.SetUser(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.language_code
            )

    await message.answer(f'Добро пожаловать !\n\nVersion: {__VERSION__}', reply_markup=await GenStart(message.chat.id))
