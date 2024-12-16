from os import remove

from aiogram import F
from aiogram.types import BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from config import config
import database.requests as rq
from database.models import Lesson
from keyboards.admins import GenDeleteLesson
from keyboards.users import __HOMEWORK__, GenLesson
from handlers.core import GetLessons, log, GetRouter
from handlers.states.lessons import FormNotificationAdmins
from utils import CheckForAdmin, NotificationAdmins, RQReporter
from keyboards.other import __BACK_IN_MAIN_MENU__, GenButtonBack


router = GetRouter()


@router.callback_query(F.data == 'lessons')
async def lessons(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    await callback.message.edit_text(text='👇 Выберете урок', reply_markup=__HOMEWORK__)


@router.callback_query(F.data.startswith('lesson:show:'))
async def lesson_show(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    await state.clear()

    calldata = callback.data.replace('lesson:show:', '')
    lesson: Lesson = await rq.GetLesson(callback.message.chat.id, calldata)

    if lesson.homework == None: lesson.homework = config.NO_FOUND_HOMEWORK_MSG

    # Photo
    if lesson.photo:
        photo = BufferedInputFile(file=lesson.photo, filename=f'image.png')
        await callback.bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=photo,
                caption=lesson.homework,
                reply_markup=await GenLesson(callback.message.chat.id, calldata, lesson.url)
            )
    else:
        await callback.message.edit_text(lesson.homework, reply_markup=await GenLesson(callback.message.chat.id, calldata, lesson.url))


@router.callback_query(F.data.startswith('lesson:nftadmins:'))
async def lesson_nftadmins_comment(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if not await CheckForAdmin(callback.message.chat.id):
        calldata: str = callback.data.replace('lesson:nftadmins:', '')

        try:
            await callback.message.edit_text('⚠️ Введите комментарий в нём можно указать на ошибку или предложить варианты исправления ошибки', 
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                [GenButtonBack('lesson:show:' + calldata)],
                                                [__BACK_IN_MAIN_MENU__]
                                            ]))
        except TelegramBadRequest:
            await callback.message.answer('⚠️ Введите комментарий в нём можно указать на ошибку или предложить варианты исправления ошибки', 
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                [GenButtonBack('lesson:show:' + calldata)],
                                                [__BACK_IN_MAIN_MENU__]
                                            ]))

        await state.set_state(FormNotificationAdmins.comment)
        await state.set_data({'lesson_id': calldata})
    else: RQReporter(callback)


@router.message(F.text, FormNotificationAdmins.comment)
async def lesson_nftadmins(message: Message, state: FSMContext):
    log.info(str(message.chat.id), msg=f'Received \'{message.text}\'')

    user = await rq.GetUser(message.chat.id, message.chat.id)

    await NotificationAdmins(
        f'⚠️ Пользователь: @{user.username} [{user.user_id}] уведомил вас в неактуальности данный по уроку \'{await GetLessons().GetName((await state.get_data())['lesson_id'])}\'\n\nКомментарий: {message.text}',
        message.bot,
        InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]])
        )

    await message.answer('✅ Отчёт отправлен. Извините за неудобства.',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                         [GenButtonBack('lessons')],
                                         [__BACK_IN_MAIN_MENU__]
                                     ]))

    await state.clear()


@router.callback_query(F.data.startswith('lesson:delete_warn:'))
async def lesson_delete_warn(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        lesson_id = callback.data.replace('lesson:delete_warn:', '')
        lesson = await rq.GetLesson(callback.message.chat.id, lesson_id)

        if lesson.homework: StatusHomework = '✅'
        else: StatusHomework = '❌'

        if lesson.photo: StatusPhoto = '✅'
        else: StatusPhoto = '❌'

        if lesson.url: StatusURL = '✅'
        else: StatusURL = '❌'
        
        try:
            await callback.message.edit_text(f'⚠️ Вы уверены ?\n\nДомашнее задание: {StatusHomework}\nФото: {StatusPhoto}\nURL: {StatusURL}', 
                                            reply_markup=await GenDeleteLesson(lesson_id))
        except TelegramBadRequest:
            await callback.message.answer(f'⚠️ Вы уверены ?\n\nДомашнее задание: {StatusHomework}\nФото: {StatusPhoto}\nURL: {StatusURL}', 
                                            reply_markup=await GenDeleteLesson(lesson_id))
    else: RQReporter(callback)


@router.callback_query(F.data.startswith('lesson:delete:'))
async def lesson_delete(callback: CallbackQuery):
    log.warn(str(callback.message.chat.id), msg=f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        lesson_id = callback.data.replace('lesson:delete:', '')

        await rq.SetLesson(callback.message.chat.id, lesson_id)

        try: remove(f'bot/database/photo/{lesson_id}.png')
        except FileNotFoundError: pass

        await callback.message.edit_text('✅ Успешно !', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [GenButtonBack(f'lesson:show:{lesson_id}')],
            [__BACK_IN_MAIN_MENU__]
        ]))
    else: RQReporter(callback)
