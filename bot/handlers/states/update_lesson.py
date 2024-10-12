from aiogram.filters.state import State, StatesGroup

class FormUpdate(StatesGroup):
    select_lesson = State()
    select_category = State()
