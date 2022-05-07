from loader import dp, hist
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command
from data import sqllite3_bd
from datetime import datetime
import asyncio




async def history(user_id):
    day_one = True
    day_two = False
    day_three = False
    day_four = False
    day_five = False
    while True:
        date_registr = await sqllite3_bd.get_date_registr(user_id)
        date_reg = datetime.strptime(str(date_registr), "%Y-%m-%d").date()
        date_now = datetime.today().date()
        difference = date_now - date_reg
        time_now = datetime.now().hour
        time_start = 12
        delay_in_second = 15 * 60
        if day_five and difference.days == 4 and time_now == time_start:
            day_namber = 5
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])
            break
        elif day_four and difference.days == 3 and time_now == time_start:
            day_namber = 4
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])
            day_four = False
            day_five = True
        elif day_three and difference.days == 2 and time_now == time_start:
            day_namber = 3
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])
            day_three = False
            day_four = True
        elif day_two and difference.days == 1 and time_now == time_start:
            day_namber = 2
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])
            day_two = False
            day_three = True
        elif day_one:
            day_namber = 1
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])
            day_one = False
            day_two = True
        await asyncio.sleep(delay_in_second)


@dp.message_handler(Command('start_history'), state=None)
async def start_hist(message: types.Message, state: FSMContext):
    if await sqllite3_bd.select_info_to_id(message.from_user.id) is None:
        await message.answer('Ты еще не прощел регистрацию!')
    else:
        await history(message.from_user.id)
