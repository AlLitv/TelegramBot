'''
По команде /homework выполняется следующий алгоритм:
получаем данные из БД и записываем их в оперативную память
и далее выводим клавиатуру. Выбираем действия с домашними работами учеников.
'''

import asyncio

from loader import dp
from aiogram import types
from aiogram.utils import exceptions
from aiogram.dispatcher.filters import Command
from data.config import teacher
from aiogram.dispatcher import FSMContext
from states import TeacherState
from data.sqllite3_bd import get_info_to_user, get_homework_user_in_date


async def get_data(state):  # получаем все данные требуемые для выполнения скриптов
    inline_keyboard = []
    info_in_us = {}
    data = await get_info_to_user()
    for id_user, surname, first_name in data:
        info_in_us[id_user] = [surname, first_name]
        inline_keyboard.append([types.InlineKeyboardButton(text=f'{surname + " " + first_name}',
                                                           callback_data=f'{id_user}')])

    for id in info_in_us.keys():
        token_file_list = {}
        info_in_us[id].append(dict(token_file_list))
        data_homework = await get_homework_user_in_date(id)
        for token_file, delivery_date in data_homework:
            try:
                info_in_us[id][2][delivery_date].append(token_file)
            except KeyError:
                info_in_us[id][2][delivery_date] = list()
                info_in_us[id][2][delivery_date].append(token_file)
    inline_keyboard.append([types.InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    async with state.proxy() as data:
        for i in info_in_us.keys():
            data[i] = info_in_us[i]
        #Формируем клавиатуры и добавляем их в оперативную память
        data['inline_keyboard'] = (inline_keyboard, len(data) + 1)
        data['markupDefaultMenu'] = types.InlineKeyboardMarkup(row_width=3,
                                                               inline_keyboard=[
                                                                   [
                                                                       types.InlineKeyboardButton(
                                                                           text="Получить ДЗ ученика",
                                                                           callback_data="getHomework")

                                                                   ],
                                                                   [
                                                                       types.InlineKeyboardButton(
                                                                           text="Ответить ученику фотографией",
                                                                           callback_data="setAnswer")
                                                                   ],
                                                                   [
                                                                       types.InlineKeyboardButton(text="Выход",
                                                                                                  callback_data="end")
                                                                   ]
                                                               ])
        data['markupFromGetInSetMenu'] = types.InlineKeyboardMarkup(row_width=2,
                                                                    inline_keyboard=[
                                                                        [
                                                                            types.InlineKeyboardButton(
                                                                                text="Ответить ученику ответ фотографией",
                                                                                callback_data="setAnswerFromGet")
                                                                        ],
                                                                        [
                                                                            types.InlineKeyboardButton(text="Отмена",
                                                                                                       callback_data="cancel")
                                                                        ]
                                                                    ])
        data['markupMenuGoodBad'] = types.InlineKeyboardMarkup(row_width=2,
                                                                    inline_keyboard=[
                                                                        [
                                                                            types.InlineKeyboardButton(
                                                                                text="Ученик ответил верно!",
                                                                                callback_data="homeworkGood")
                                                                        ],
                                                                        [
                                                                            types.InlineKeyboardButton(
                                                                                text="Ученик ответил не верно!",
                                                                                callback_data="homeworkBad")
                                                                        ],
                                                                        [
                                                                            types.InlineKeyboardButton(text="Отмена",
                                                                                                       callback_data="cancel")
                                                                        ]
                                                                    ])


@dp.message_handler(Command('homework'), user_id=teacher)
async def start_get_homework(message: types.Message, state: FSMContext):
    await get_data(state)
    async with state.proxy() as data:
        await message.answer("Что хотите сделать?", reply_markup=data['markupDefaultMenu'])
        await TeacherState.default.set()


@dp.callback_query_handler(user_id=teacher, text_contains="cancel", state="*")
async def default_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.delete()
    async with state.proxy() as data:
        await call.message.answer("Что хотите сделать?", reply_markup=data['markupDefaultMenu'])
    await TeacherState.default.set()

# Получаем домашнюю работу ученик
@dp.callback_query_handler(user_id=teacher, text_contains="getHomework", state=TeacherState.default)
async def get_homeworks(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.edit_reply_markup()
        await call.message.delete()
        markupMenuUse = types.InlineKeyboardMarkup(row_width=data['inline_keyboard'][1],
                                                   inline_keyboard=data['inline_keyboard'][0])
        await call.message.answer('Получить домашнюю работу:', reply_markup=markupMenuUse)
        await TeacherState.choose_date.set()


# Получаем список дат и домашних работ учеников в эти даты
@dp.callback_query_handler(user_id=teacher, state=TeacherState.choose_date)
async def get_homeworks(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.edit_reply_markup()
        await call.message.delete()
        inline_keyboard = []

        id_user = int(call.data)  # получаем id пользователя которого выбрал учитель
        for date in data[id_user][2].keys():
            inline_keyboard.append([types.InlineKeyboardButton(text=f'{date}',
                                                               callback_data=f'{str(id_user) + " " + date}')])
        inline_keyboard.append([types.InlineKeyboardButton(text="Отмена", callback_data="cancel")])
        markupMenuDate = types.InlineKeyboardMarkup(row_width=len(data[id_user][2]) + 1,
                                                    inline_keyboard=inline_keyboard)
        await call.message.answer('Даты в которые ученик сдал дз:', reply_markup=markupMenuDate)
        await TeacherState.get_homework.set()

#Отправка ответа учителю в зависимости от его выбора
@dp.callback_query_handler(user_id=teacher, state=TeacherState.get_homework)
async def get_homeworks(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    id, key = call.data.split()
    await call.message.delete()
    async with state.proxy() as data:
        for photo in data[int(id)][2][key]:
            await dp.bot.send_photo(chat_id=teacher, photo=photo)
            await asyncio.sleep(0.1)
        await call.message.answer("Что дальше?", reply_markup=data['markupFromGetInSetMenu'])
        data['activ_student'] = int(id)
        await TeacherState.default.set()

#Если отправляем ответ то ожидаем фото проверенной работы
@dp.callback_query_handler(user_id=teacher, text_contains="setAnswerFromGet", state=TeacherState.default)
async def set_homework_result(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.delete()
    await call.message.answer("Отправьте мне фото!")
    await TeacherState.expect_photo.set()


@dp.callback_query_handler(user_id=teacher, text_contains="setAnswer", state=TeacherState.default)
async def choise_student(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.delete()
    async with state.proxy() as data:
        markupMenuUse = types.InlineKeyboardMarkup(row_width=data['inline_keyboard'][1],
                                                   inline_keyboard=data['inline_keyboard'][0])
        await call.message.answer("Кому отправить результат?", reply_markup=markupMenuUse)
        await TeacherState.setAnswer.set()


@dp.callback_query_handler(user_id=teacher, state=TeacherState.setAnswer)
async def set_homewor_result(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    key = call.data
    await call.message.delete()
    async with state.proxy() as data:
        data['activ_student'] = key
        await call.message.answer("Отправьте мне фото!")
        await TeacherState.expect_photo.set()


@dp.message_handler(user_id=teacher, content_types=['photo'], state=TeacherState.expect_photo)
async def set_homework_result(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            await dp.bot.send_message(chat_id=int(data['activ_student']), text="Твоя работа проверенна!")
            await dp.bot.send_photo(chat_id=int(data['activ_student']), photo=message.photo[-1].file_id)
            await message.answer("Работа отправлена!Что делаем дальше?", reply_markup=data['markupDefaultMenu'])
            data['activ_student'] = None
        await TeacherState.default.set()
    except exceptions.BotBlocked:
        await message.answer("Не удалось отправить фото! Пользователь заблокировал меня! Может что то еще?",
                             reply_markup=data['markupDefaultMenu'])
        await TeacherState.default.set()
    except Exception as err:
        print(err)


@dp.callback_query_handler(user_id=teacher, text_contains="end", state="*")
async def end_examination(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.delete()
    await call.message.answer("Увидимся!")
    await state.finish()
    await state.reset_state()
