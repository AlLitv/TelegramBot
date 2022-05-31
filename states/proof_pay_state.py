from aiogram.dispatcher.filters.state import StatesGroup, State



class Proof_state_pay(StatesGroup):
    default_pay = State()
    proof_paymet = State()
    remind_payment = State()
    choise_action = State()
