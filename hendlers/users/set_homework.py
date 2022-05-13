import time
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import admin_id, teacher
from data import sqllite3_bd
import datetime
from states.homework import Questions_homework

markupKebord = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
                                                                   [
                                                                       types.InlineKeyboardButton(
                                                                           text="Да",
                                                                           callback_data="yes"),
                                                                       types.InlineKeyboardButton(
                                                                           text="Нет",
                                                                           callback_data="no")

                                                                   ],
                                                                   [
                                                                       types.InlineKeyboardButton(text="Выход",
                                                                                                  callback_data="end")
                                                                   ]
                                                               ])




@dp.message_handler(Command('Submit_homework'), state=None)
async def start_submit_homework(message: types.Message, state: FSMContext):
    if await sqllite3_bd.select_info_to_id(message.from_user.id) is None:
        await message.answer('Ты еще не прошел регистрацию!\n'
                             'Введи команду /registrs что бы это сделать!')
        await state.finish()
    else:
        await message.answer("Для того что бы сдать домашнее задание отправь фото работы мне.",
                             reply_markup=types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                                                       [
                                                                       types.InlineKeyboardButton(text="Выход",
                                                                                                  callback_data="end")
                                                                       ]
                                                                    ]))
        await Questions_homework.set_photo.set()


@dp.callback_query_handler(text_contains="end", state='*')
async def end_set_homework(call: types.CallbackQuery, state:FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("Приходи как доделаешь!")
    await state.finish()




@dp.message_handler(content_types=['photo'], state=Questions_homework.set_photo)
async def seting_photo(message: types.Message, state:FSMContext):
    if not await state.get_data():
        await state.update_data(photo=[message.photo[-1].file_id])
        await message.answer("Ты отправил нужное фото?", reply_markup=markupKebord)
        await Questions_homework.end_homework.set()
    else:
        my_list = await state.get_data()
        photos = my_list.get("photo")
        photos.append(message.photo[-1].file_id)
        await state.update_data(photo=photos)
    # async with state.proxy() as data:
    #     data["photo"] = message.photo[0].file_id
    # await message.answer("Ты отправил нужное фото?")
    # await Questions_homework.end_homework.set()


@dp.callback_query_handler(state=Questions_homework.end_homework)
async def finished_submit(call: types.CallbackQuery, state:FSMContext):
    answer = call.data
    await call.message.edit_reply_markup()
    if answer == 'yes':
        await call.message.answer("Отлично! Скоро узнаешь результат!")
        async with state.proxy() as data:
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            for i in data['photo']:
                await sqllite3_bd.add_info_bd_homework("users_homework", i, call.from_user.id, date)
            await dp.bot.send_message(chat_id=teacher, text='Ученик отправил вам домашнее задание')
            #await dp.bot.send_photo(chat_id=448768892, photo=data['photo'])
        await state.finish()
    elif answer == 'no':
        await call.message.answer("Давай попробуем еще раз! Отпраляй фото!")
        await Questions_homework.set_photo.set()



