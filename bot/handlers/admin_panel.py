from platform import system, release, python_version

import psutil
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from handlers.core import log, GetRouter
from utils import CheckForAdmin, RQReporter, newsletter
from handlers.states.newsletter import FormNewsletter
from keyboards.other import GenButtonBack, __BACK_IN_MAIN_MENU__
from keyboards.admins import __ADMIN_PANEL__, __NEWSLETTER_WARN__


router = GetRouter()


@router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        log.warn(callback.message.chat.id, 'Admin logged into the panel . . .')
        
        await callback.message.edit_text('🛠Вы в админ-панели!\nБудьте осторожны‼️', reply_markup=__ADMIN_PANEL__)

        await state.clear()
    else: RQReporter(callback)


@router.callback_query(F.data == 'admin_panel:newsletter_input')
async def admin_panel_newsletter_input(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        await callback.message.edit_text('Введите текст рассылки')
        await state.set_state(FormNewsletter.input_text)
    else: RQReporter(callback)


@router.message(F.text, FormNewsletter.input_text)
async def admin_panel_form_newsletter_input_text(message: Message, state: FSMContext):
    log.info(str(message.chat.id), msg=f'Received \'{message.text}\'')

    if await CheckForAdmin(message.chat.id):
        await message.answer(f'<b>‼️ВЫ ТОЧНО ХОТИТЕ ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ ПОЛЬЗОВАТЕЛЯМ⁉️</b>\nТЕКСТ СООБЩЕНИЯ:\n{message.text}', 
                             reply_markup=__NEWSLETTER_WARN__)

        await state.set_state(FormNewsletter.warn)
        await state.set_data({'text': message.text})



@router.callback_query(F.data == 'admin_panel:newsletter', FormNewsletter.warn)
async def admin_panel_newsletter(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')
    
    if await CheckForAdmin(callback.message.chat.id):
        await callback.message.edit_text('✅ Рассылка началась!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [GenButtonBack('admin_panel')],
            [__BACK_IN_MAIN_MENU__]
        ]))

        await newsletter(callback.message.chat.id, str((await state.get_data())['text']), False, callback.message.bot)
    else: RQReporter(callback)


@router.callback_query(F.data == 'admin_panel:status_server')
async def admin_panel_status_server(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if await CheckForAdmin(callback.message.chat.id):
        log.info(callback.message.chat.id, 'Admin requested a server status report, generation . . .')  

        log.debug(callback.message.chat.id, 'Generating information about: SystemName')
        SystemName = str(system())

        log.debug(callback.message.chat.id, 'Generating information about: SystemRelease')
        SystemRelease = str(RELEASE)

        log.debug(callback.message.chat.id, 'Generating information about: PythonVersion')
        PythonVersion = str(python_version())

        # Загруженость
        # CPU
        log.debug(callback.message.chat.id, 'Generating information about: CPU')
        CPU = psutil.cpu_percent(interval=1)

        # Memory
        log.debug(callback.message.chat.id, 'Generating information about: Memory, Memory_Swap')
        Memory = psutil.virtual_memory()
        Memory_Swap = psutil.swap_memory()

        # Disks
        log.debug(callback.message.chat.id, 'Generating information about: Disks')
        Disks = psutil.disk_usage('/')

        # Network
        log.debug(callback.message.chat.id, 'Generating information about: Network')
        all_interf = psutil.net_if_addrs()
        Network: str = '\n'

        for interf in all_interf:
            Network = f'{Network}- {interf}: {all_interf[interf][0][1]}\n'

        log.info(callback.message.chat.id, 'Generating a report based on the data received . . .')
        
        report = f'OS: {SystemName} {SystemRelease}\nPython: {PythonVersion}\n\nЗагруженость:\n\nCPU: {CPU}%\nMemory: {Memory.percent}%\nMemory Swap: {Memory_Swap.percent}%\nDisks: {Disks.percent}%\nNetwork: {Network}'
        
        log.info(callback.message.chat.id, 'Successfully !')

        await callback.message.edit_text(report, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[GenButtonBack('admin_panel')], [__BACK_IN_MAIN_MENU__]]))

        log.info(callback.message.chat.id, 'Report Sent !')
    else: RQReporter(callback)
