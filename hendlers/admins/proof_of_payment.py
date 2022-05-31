from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import admin_id
from aiogram.utils import exceptions
from aiogram.dispatcher import FSMContext
from states import Proof_state_pay
from data.sqllite3_bd import get_full_name_from_db, get_info_to_user_no_pay, set_pay_status_yes


async def get_no_pay_user(): # получаем все данные требуемые для выполнения скриптов
    data = await get_info_to_user_no_pay()
    inline_keyboard = types.InlineKeyboardMarkup()
    counter_line = 1
    for id_user, surname, first_name in data:
        counter_line += 1
        inline_keyboard.inline_keyboard.append([types.InlineKeyboardButton(text=f'{surname + " " + first_name}',
                                                        callback_data=f'{id_user}')])

    inline_keyboard.inline_keyboard.append([types.InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    inline_keyboard.row_width = counter_line
    return inline_keyboard


async def gen_keyboard_state_start_proof():
    markupKebord = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Подтвердить оплату",
                callback_data="proof_pay"),
            types.InlineKeyboardButton(
                text="Напомнить об оплате!",
                callback_data="remind_payment")
        ],
        [
            types.InlineKeyboardButton(text="Выход",
                                       callback_data="end")
        ]
    ])
    return markupKebord

async def gen_keyboard_confirmation():
    markupKebord = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Да",
                callback_data="yes")
        ],
        [
            types.InlineKeyboardButton(text="Отмена",
                                       callback_data="cancel")
        ]
    ])
    return markupKebord



@dp.message_handler(Command('payment'))
async def start_proof_pay(message: types.Message):
    if message.from_user.id in admin_id:
        markupKeyboard = await gen_keyboard_state_start_proof()
        await message.answer(text="Меню оплаты!\nВыбор действия", reply_markup=markupKeyboard)
        await Proof_state_pay.default_pay.set()
    else:
        await message.answer("Вы не являетесь администратором!")


@dp.callback_query_handler(text_contains="end", state=Proof_state_pay.default_pay)
async def choise_student(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text_contains="cancel", state="*")
async def choise_student(call: types.CallbackQuery):
    await call.message.delete()
    markupday = await gen_keyboard_state_start_proof()
    await call.message.answer(text="Меню оплаты!\nВыбор действия", reply_markup=markupday)
    await Proof_state_pay.default_pay.set()


@dp.callback_query_handler(text_contains="proof_pay", state=Proof_state_pay.default_pay)
async def choise_student(call: types.CallbackQuery):
    await call.message.delete()
    markupKey = await get_no_pay_user()
    await call.message.answer("Нет оплаты:", reply_markup=markupKey)
    await Proof_state_pay.proof_paymet.set()


@dp.callback_query_handler(text_contains="yes", state=Proof_state_pay.proof_paymet)
async def proof_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        id_student = data['activ_student']
    await dp.bot.send_message(chat_id=int(id_student), text="Оплата подтверждена! Вводи /start_history и скорее начинаем!")
    full_name = await get_full_name_from_db(id_student)
    keyboard = await gen_keyboard_state_start_proof()
    await call.message.answer(f"{full_name} оплата подтверждена! Что то еще?", reply_markup=keyboard)
    await set_pay_status_yes(id_student)
    await Proof_state_pay.default_pay.set()


@dp.callback_query_handler(state=Proof_state_pay.proof_paymet)
async def proof_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['activ_student'] = call.data
    keyboard = await gen_keyboard_confirmation()
    await call.message.answer(text="Вы действительно хотите это сделать?", reply_markup=keyboard)


@dp.callback_query_handler(text_contains="remind_payment", state=Proof_state_pay.default_pay)
async def choise_student(call: types.CallbackQuery):
    await call.message.delete()
    reply_markup = await get_no_pay_user()
    await call.message.answer("Нет оплаты:", reply_markup=reply_markup)
    await Proof_state_pay.remind_payment.set()


@dp.callback_query_handler(text_contains="yes", state=Proof_state_pay.remind_payment)
async def proof_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        id_student = data['activ_student']
    full_name = await get_full_name_from_db(id_student)
    keyboard = await gen_keyboard_state_start_proof()
    try:
        await dp.bot.send_message(chat_id=id_student, text="Я жду оплату! \n Если ты уже оплатил, "
                                                 "то подожди немного, скоро начнем!")
        await call.message.answer(f"{full_name} напоминамие об оплате отправлено!", reply_markup=keyboard)
    except exceptions.BotBlocked:
        await call.message.answer(f"Не удалось отправить напоминание! Пользователь {full_name} заблокировал меня!"
                                  f" Может еще что то?",
                                  reply_markup=keyboard)
    await Proof_state_pay.default_pay.set()


@dp.callback_query_handler(state=Proof_state_pay.remind_payment)
async def proof_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['activ_student'] = call.data
    keyboard = await gen_keyboard_confirmation()
    await call.message.answer("Вы действительно хотите это сделать?", reply_markup=keyboard)








