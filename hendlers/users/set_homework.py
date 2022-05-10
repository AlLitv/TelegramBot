import time
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import admin_id
from data import sqllite3_bd
import datetime






from states.homework import Questions_homework



@dp.message_handler(Command('Submit_homework'), state=None)
async def start_submit_homework(message: types.Message, state: FSMContext):
    await message.answer("Для того что бы сдать домашнее задание отправь фото работы мне.")
    await Questions_homework.set_photo.set()



@dp.message_handler(content_types=['photo'], state=Questions_homework.set_photo)
async def seting_photo(message: types.Message, state:FSMContext):
        if not await state.get_data():
            await state.update_data(photo=[message.photo[-1].file_id])
            await message.answer("Ты отправил нужное фото?")
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


@dp.message_handler(content_types=['text'], state=Questions_homework.end_homework)
async def finished_submit(message: types.Message, state:FSMContext):
    if message.text.lower() == 'да':
        await message.answer("Отлично! Скоро узнаешь результат!")
        async with state.proxy() as data:
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            for i in data['photo']:
                await sqllite3_bd.add_info_bd_homework("users_homework", i, message.from_user.id, date)
            await dp.bot.send_message(chat_id=448768892, text='Ученик отправил вам домашнее задание')
            #await dp.bot.send_photo(chat_id=448768892, photo=data['photo'])
        await state.finish()

    elif message.text.lower() == 'нет':
        await message.answer("Давай попробуем еще раз! Отпраляй фото!")
        await Questions_homework.set_photo.set()