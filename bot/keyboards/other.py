from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.lessons import Lessons

__BACK_IN_MAIN_MENU__: InlineKeyboardButton = InlineKeyboardButton(text='⏪ Вернуться в главное меню', callback_data='menu')


def GenButtonBack(callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text='⬅️  Назад', callback_data=callback_data)


def GenLesson(lessons: Lessons, appstart_text: str = '', append_text: str = '', appstart_callback_data: str = '', append_callback_data: str = '') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for lesson in lessons.lessons:
        builder.row(InlineKeyboardButton(text=appstart_text + lesson[1] + append_text, callback_data=appstart_callback_data + lesson[0] + append_callback_data))

    builder.adjust(3)
    return builder.as_markup()


def CheckCallBackData(input: str, append_callback_data: str) -> bool:
    for lesson in Lessons().lessons:
        if input == str(lesson[0] + append_callback_data): return True

    return False
