from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

import database.requests as rq
from handlers.core import log, GetRouter
from utils import CheckForAdmin, CheckAuthUser
from keyboards.other import GenButtonBack, __BACK_IN_MAIN_MENU__
from keyboards.users import GenProfile, __OFF__NOTIFICATIONS__


router = GetRouter()


@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    await CheckAuthUser(callback.message, callback.message.bot)

    user = await rq.GetUser(callback.message.chat.id, callback.message.chat.id)
    net_school = await rq.GetNetSchool(callback.message.chat.id, False)

    if user.send_notifications: notifications_status = '✅'
    else: notifications_status = '❌'

    if net_school: net_school_status = '✅'
    else: net_school_status = '❌'

    if await CheckForAdmin(callback.message.chat.id): isAdmin = '✅'
    else: isAdmin = '❌'

    await callback.message.edit_text(f'Ваш никнейм: {user.first_name}\nВаше имя: @{user.username}\nTELEGRAM-ID: {user.user_id}\n\nУведомления: {notifications_status}\nИнтеграция с СГО: {net_school_status}\nПрава администратора: {isAdmin}',
                                     reply_markup=await GenProfile(user.send_notifications, net_school))


@router.callback_query(F.data == 'profile:notifications:off_warn')
async def profile_notifications_off_warn(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    await CheckAuthUser(callback.message, callback.message.bot)

    await callback.message.edit_text('Вы уверены ?\n\n*Если вы отключите уведомления вы не будете получать сообщения об обновлении домашнего задания и расписания. Сюда НЕ входит рассылка от администраторов бота.', reply_markup=__OFF__NOTIFICATIONS__)


@router.callback_query(F.data == 'profile:notifications:off')
async def profile_notifications_off(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    await CheckAuthUser(callback.message, callback.message.bot)

    await rq.SetSendNotifications(callback.message.chat.id, False)
    await callback.message.edit_text('✅ Успешно! Вы больше не будете получать уведомления.',
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[[GenButtonBack('profile')], [__BACK_IN_MAIN_MENU__]]))


@router.callback_query(F.data == 'profile:notifications:on')
async def profile_notifications_on(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    await CheckAuthUser(callback.message, callback.message.bot)

    await rq.SetSendNotifications(callback.message.chat.id, True)
    await callback.message.edit_text('✅ Успешно! Вы будете получать уведомления.',
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[[GenButtonBack('profile')], [__BACK_IN_MAIN_MENU__]]))
