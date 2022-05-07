from aiogram.dispatcher.filters.state import StatesGroup, State



class AdminState(StatesGroup):
    menuAdmin = State()
    day_state = State()
    text = State()
    file = State()
    stick = State()
    video = State()
    end = State()

