from aiogram.dispatcher.filters.state import StatesGroup, State



class Questions_registrs(StatesGroup):
    questions_name = State()
    questions_surname = State()
    questions_age = State()
    questions_class = State()
    end_registr = State()
    error_enter = State()
    error_name = State()
    error_surname = State()
    error_age = State()
    error_class = State()
    pay = State()

