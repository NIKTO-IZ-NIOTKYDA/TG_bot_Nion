from os import remove

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

import bot.database.requests as rq
from bot.handlers.core import log, GetRouter
from bot.config import __TEMP_PHOTO_PATH_FILE__
from bot.keyboards.other import __BACK_IN_MAIN_MENU__
from bot.handlers.states.update_lesson import FormUpdate
from bot.utils import CheckForAdmin, RQReporter, SendUpdateLesson, rename
from bot.keyboards.admins import __UPDATE_MENU__, __UPDATE_HOMEWORK__, __UPDATE_URL__


router = GetRouter()


@router.message(F.text)
async def update_select_category(message: Message, state: FSMContext) -> None:
    log.info(str(message.chat.id), f'Received \'{message.text}\'')

    if await CheckForAdmin(message.chat.id):
        await message.answer('Где нужно поставить этот текст ?', reply_markup=__UPDATE_MENU__)
        
        await state.set_state(FormUpdate.select_category)
        await state.set_data({'text': message.text})


@router.callback_query(F.data, FormUpdate.select_category)
async def update_select_lesson(callback: CallbackQuery, state: FSMContext) -> None:
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        if callback.data == 'update:homework':
            await callback.message.edit_text('👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=__UPDATE_HOMEWORK__)
        elif callback.data == 'update:url':
            await callback.message.edit_text('👇 Выберете предмет по которому хотите заменить ГДЗ', reply_markup=__UPDATE_URL__)

        await state.set_state(FormUpdate.select_lesson)
    else: RQReporter(callback)


@router.callback_query(F.data != 'paragraph', FormUpdate.select_lesson)
async def update(callback: CallbackQuery, state: FSMContext) -> None:
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        await callback.message.edit_text('⚙️ Выполняется замена, пожалуйста, подождите . . .')

        lesson_id = callback.data.split(':')[-1]

        if callback.data.startswith('update:homework:'):   
            await rq.SetLesson(
                callback.message.chat.id,
                lesson_id,
                homework=(await state.get_data())['text']
                )

            try: remove('photo/' + lesson_id + '.png')
            except FileNotFoundError: pass

            await callback.message.edit_text('✅ Успешно !')

            await callback.message.edit_text('⚠ Активирована система уведомлений . . .', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
            await SendUpdateLesson(callback.message.chat.id, lesson_id, bot=callback.bot)
        elif callback.data.startswith('update:homework_and_photo:'):
            await rename(callback.message.chat.id, file_name_in=__TEMP_PHOTO_PATH_FILE__, file_name_out=f'bot/database/photo/{lesson_id}.png')

            await rq.SetLesson(
                callback.message.chat.id,
                lesson_id,
                homework=(await state.get_data())['homework'],
                photo=True
            )

            await callback.message.edit_text('✅ Успешно !')

            await callback.message.edit_text('⚠ Активирована система уведомлений . . .', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
            await SendUpdateLesson(callback.message.chat.id, lesson_id, bot=callback.bot)
        elif callback.data.startswith('update:url:'):
            lesson = await rq.GetLesson(callback.message.chat.id, lesson_id)

            await rq.SetLesson(
                callback.message.chat.id,
                lesson_id,
                homework=lesson.homework,
                photo=lesson.photo,
                url=(await state.get_data())['text']
            )

            await callback.message.edit_text('✅ Успешно !', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
    else: RQReporter(callback)


@router.callback_query(F.data == 'paragraph')
async def paragraph(callback: CallbackQuery) -> None:
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')
    
    await callback.message.edit_text('§\n\n#paragraph')
