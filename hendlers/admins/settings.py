from loader import dp, hist
from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import admin_id
from aiogram.dispatcher import FSMContext
from states import AdminState
import sqlite3
from data.sqllite3_bd import add_info_bd_content

markupmenu = types.InlineKeyboardMarkup(row_width=4,
                                        inline_keyboard=[
                                            [types.InlineKeyboardButton(text="Добавить текст", callback_data="text")],
                                            [types.InlineKeyboardButton(text="Добавить стикер", callback_data="stick")],
                                            [
                                                types.InlineKeyboardButton(text="Добавить файл дз", callback_data="file"),
                                                types.InlineKeyboardButton(text="Добавить видео", callback_data="video")
                                             ],
                                            [types.InlineKeyboardButton(text="Закончить", callback_data="end")]
                                        ])

markupday = types.InlineKeyboardMarkup(row_width=3,
                                       inline_keyboard=[
                                           [
                                               types.InlineKeyboardButton(text="Прервый день", callback_data=1),
                                               types.InlineKeyboardButton(text="Второй день", callback_data=2)
                                           ],
                                           [
                                               types.InlineKeyboardButton(text="Третий день", callback_data=3),
                                               types.InlineKeyboardButton(text="Четвертый день", callback_data=4)
                                           ],
                                           [
                                               types.InlineKeyboardButton(text="Пятый день", callback_data=5),
                                               types.InlineKeyboardButton(text="Шестой день", callback_data=6)
                                           ]
                                       ])


@dp.message_handler(Command('settings'))
async def open_settings(message: types.Message, state: FSMContext): # Вход в режим администратора
    if message.from_user.id in admin_id:
        await message.answer("Вы в режиме администратора!")
        await message.answer(text="В какой из дней внести изменения?", reply_markup=markupday)
        async with state.proxy() as data:
            data['day'] = None  #Обнуляем номер дня в котором будем вносить изменения
        await AdminState.day_state.set()
    else:
        await message.answer("Вы не являетесь администратором!")


@dp.callback_query_handler(state=AdminState.day_state)
async def choice_day(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    async with state.proxy() as data:
        data['day'] = call.data # Записываем данные в память номер выбранного дня
    await call.message.answer(text="Что хотите изменить?", reply_markup=markupmenu) #Выбираем текст контекста
    await AdminState.menuAdmin.set()


@dp.callback_query_handler(text_contains="text", state=AdminState.menuAdmin) #Получаем текст
async def admin_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(text="Введите текст сообщения!")
    await AdminState.text.set()


@dp.message_handler(content_types=["text"], state=AdminState.text) # Обрабатываем текст
async def enter_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await add_info_bd_content(data['day'], # Записываем текст и номер дня в базу данных
                                  'text',
                                  message.text

                                  )
    await message.answer(text="Что хотите изменить?", reply_markup=markupmenu)
    await AdminState.menuAdmin.set()


@dp.callback_query_handler(text_contains="stick", state=AdminState.menuAdmin)
async def admin_menu__(call: types.CallbackQuery, state: FSMContext): # Принемаем стикер для обработки
    await call.message.edit_reply_markup()
    await call.message.answer(text="Отправьте стикер")
    await AdminState.stick.set()


@dp.message_handler(content_types=types.ContentType.STICKER, state=AdminState.stick)
async def enter_stick(message: types.Message, state: FSMContext): #Обрабатываем стикер
    async with state.proxy() as data:
        await add_info_bd_content(data['day'], # Записываем в БД стикер
                                  'stiker_id',
                                  message.sticker.file_id
                                  )
    await message.answer(text="Что хотите изменить?", reply_markup=markupmenu)
    await AdminState.menuAdmin.set()


@dp.callback_query_handler(text_contains="file", state=AdminState.menuAdmin)
async def admin_menu_(call: types.CallbackQuery, state: FSMContext): #Получаем фото
    await call.message.edit_reply_markup()
    await call.message.answer(text="Отправьте фото")
    await AdminState.file.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=AdminState.file)
async def enter_photo(message: types.Message, state: FSMContext):#Обрабатываем фото
    async with state.proxy() as data:
        await add_info_bd_content(data['day'],#Отправляем фото в БД
                                  'photo_id',
                                  message.photo[-1].file_id)
    await message.answer(text="Что хотите изменить?", reply_markup=markupmenu)
    await AdminState.menuAdmin.set()


@dp.callback_query_handler(text_contains="video", state=AdminState.menuAdmin)
async def admin_menu(call: types.CallbackQuery, state: FSMContext): #Получаем видео
    await call.message.edit_reply_markup()
    await call.message.answer(text="Отправь нужное видео")
    await AdminState.video.set()


@dp.message_handler(content_types=["video"], state=AdminState.video)
async def add_video(message: types.Message, state: FSMContext):#Обрабатываем видео файл
    async with state.proxy() as data:
        await add_info_bd_content(data['day'],#Отправляем видео в БД
                                  'video',
                                  message.video.file_id
                                  )
        await message.answer(text="Что хотите изменить?", reply_markup=markupmenu)
        await AdminState.menuAdmin.set()


@dp.callback_query_handler(text_contains="end", state=AdminState.menuAdmin)
async def enter_text(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="Редактирование завершено")
    await call.message.edit_reply_markup()
    await hist.fill_in_data()
    await state.finish()

