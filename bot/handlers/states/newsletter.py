from aiogram.filters.state import State, StatesGroup

class FormNewsletter(StatesGroup):
    input_text = State()
    warn = State()
