from aiogram.dispatcher.filters.state import StatesGroup, State


class TeacherState(StatesGroup):
    get_homework = State()
    cancel = State()
    default = State()
    setAnswer = State()
    expect_photo = State()
    end = State()
