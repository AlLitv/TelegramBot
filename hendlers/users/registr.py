from aiogram.dispatcher.storage import FSMContextProxy
from  data.config import logger
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import admin_id, teacher
from data import sqllite3_bd
import datetime

from states.registers import Questions_registrs

markupKebordPay = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
                                                                   [
                                                                       types.InlineKeyboardButton(
                                                                           text="Да",
                                                                           callback_data="yes"),
                                                                       types.InlineKeyboardButton(
                                                                           text="Нет",
                                                                           callback_data="no")

                                                                   ]
                                                               ])

async def message_end_registr(message, data):
    await message.answer('Регистрация завершна! Проверьте введнные данные!')
    await message.answer(f"Тебя зовут: {data['name']}\n"
                         f"Твоя фамилия: {data['surname']}\n"
                         f"Тебе {data['age']} лет\n"
                         f"Ты учишься в {data['class']} классе\n"
                         f"Все верно?")
    await Questions_registrs.end_registr.set()


@dp.message_handler(Command('registrs'), state=None)
async def start_registers(message: types.Message, state: FSMContext):
    if await sqllite3_bd.select_info_to_id(message.from_user.id) is None:
        await Questions_registrs.questions_name.set()
        await message.answer('Ты начал регистрацию! '
                            'Введи свое имя.')
        text = 'startig new user registration'
        logger.info(text)
        await dp.bot.send_message(chat_id=admin_id[0], text=text)
    else:
        await message.answer("Ты уже зарегистрирован!")
        await state.finish()



@dp.message_handler(content_types=['text'], state=Questions_registrs.questions_name)
async def name_registers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Введи фамилию')
    await Questions_registrs.questions_surname.set()


@dp.message_handler(content_types=['text'], state=Questions_registrs.questions_surname)
async def surname_registers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await message.answer('Сколько тебе лет?')
    await Questions_registrs.questions_age.set()


@dp.message_handler(content_types=['text'], state=Questions_registrs.questions_age)
async def age_registers(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['age'] = int(message.text)
            await message.answer('В каком классе ты учишься? Напиши только цифру!Если не учишься в школе введи 0')
            await Questions_registrs.questions_class.set()
    except ValueError:
        await message.answer('Ты ввел не число! Попробуй еще раз!')


@dp.message_handler(content_types=['text'], state=Questions_registrs.questions_class)
async def age_registers(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['class'] = int(message.text)
            await message.answer('Регистрация завершна! Проверьте введнные данные!')
            await message.answer(f"Тебя зовут: {data['name']}\n"
                                 f"Твоя фамилия: {data['surname']}\n"
                                 f"Тебе {data['age']} лет\n"
                                 f"Ты учишься в {data['class']} классе\n"
                                 f"Все верно?")
            await Questions_registrs.end_registr.set()
    except ValueError:
        await message.answer('Ты ввел не число! Попробуй еще раз!')


@dp.message_handler(content_types=['text'], state=Questions_registrs.end_registr)
async def end_registrs(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer('Спасибо за регистрацию!Для того что бы история началась оплати 1000р по ссылке\n'
                             '\nhttps://www.tinkoff.ru/rm/litvinova.natalya256/gSr9A90857\n'
                             'Обязательно в коментариях укажи фамилию и имя участника смены\n'
                             'Только с 1 по 5 июня действует скидка <b>50%</b>\n'
                             'Ожидайте подтверждения оплаты!\n'
                             'Если возникли сложности напишите @natali_shumilo_repetitor',
                             parse_mode='html')
        async with state.proxy() as data:
            age = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            await sqllite3_bd.set_pay_status_none(message.from_user.id)
            await sqllite3_bd.add_info_bd("users",
                                            message.from_user.id,
                                                     data['name'],
                                                     data['surname'],
                                                     data['class'],
                                                     data['age'],
                                                     date
                                                     )
            logger.info(f"registration completed NAME: {data['name']} SURNAME: {data['surname']} CLASS: {data['class']}"
                        f"ID: {message.from_user.id}")
            await dp.bot.send_message(chat_id=admin_id[1], text=f'Пользователь {data["name"] + " " + data["surname"]}'
                                                                f' Подтвердите оплату.')
        await state.finish()
    elif message.text.lower() == "нет":
        await message.answer('Где ты ошибся?'
                             'В имени?'
                             'В фамилии?'
                             'В возрасте?'
                             'В классе?')
        await Questions_registrs.error_enter.set()




@dp.message_handler(content_types=['text'], state=Questions_registrs.error_enter)
async def questions_error(message: types.Message):
    if message.text.lower() == "в имени":
        await message.answer('Введи имя заново')
        await Questions_registrs.error_name.set()
    elif message.text.lower() == "в фамилии":
        await message.answer('Введи фамилию заново')
        await Questions_registrs.error_surname.set()
    elif message.text.lower() == "в возрасте":
        await message.answer('Введи возраст заново')
        await Questions_registrs.error_age.set()
    elif message.text.lower() == "в классе":
        await message.answer('Введи класс заново')
        await Questions_registrs.error_class.set()


@dp.message_handler(content_types=['text'], state=Questions_registrs.error_name)
async def name_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message_end_registr(message, data)


@dp.message_handler(content_types=['text'], state=Questions_registrs.error_surname)
async def surname_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
        await message_end_registr(message, data)


@dp.message_handler(content_types=['text'], state=Questions_registrs.error_age)
async def age_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
        await message_end_registr(message, data)


@dp.message_handler(content_types=['text'], state=Questions_registrs.error_class)
async def class_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['class'] = message.text
        await message_end_registr(message, data)
