from aiogram.types import Message
from aiogram.filters import Command

from config import config
import database.requests as rq
from utils import CheckAuthUser
from keyboards.users import GenStart
from handlers.core import log, GetRouter


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

    await message.answer(f'Добро пожаловать !\n\nVersion: {config.GetRELEASE}', reply_markup=await GenStart(message.chat.id))
