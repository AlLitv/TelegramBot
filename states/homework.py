from aiogram.dispatcher.filters.state import StatesGroup, State



class Questions_homework(StatesGroup):
    set_photo = State()
    end_homework = State()