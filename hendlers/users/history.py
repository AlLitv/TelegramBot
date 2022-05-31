from loader import dp, hist
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command
from data.sqllite3_bd import get_user_pay
from datetime import datetime, date
import asyncio




async def history(user_id):
    day_one = True
    day_two = False
    day_three = False
    day_four = False
    day_five = False
    day_six = False
    date_start: date = datetime.today().date()
    while True:
        #date_registr = await sqllite3_bd.get_date_registr(user_id)
        #date_reg = datetime.strptime(str(date_registr), "%Y-%m-%d").date()
        date_now = datetime.today().date()
        difference = date_now - date_start
        time_now = datetime.now().hour
        time_start = 23
        delay_in_second = 6
        difference_days = difference.days
        if day_six and difference_days == 5 and time_now == time_start:
            day_namber = 6
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            break
        elif day_five and difference_days == 4 and time_now == time_start:
            day_namber = 5
            day_five = False
            day_six = True
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])
        elif day_four and difference_days == 3 and time_now == time_start:
            day_namber = 4
            day_four = False
            day_five = True
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])

        elif day_three and difference_days == 2 and time_now == time_start:
            day_namber = 3
            day_three = False
            day_four = True
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])

        elif day_two and difference_days == 1 and time_now == time_start:
            day_namber = 2
            day_two = False
            day_three = True
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
            await dp.bot.send_photo(chat_id=user_id, photo=hist.file[day_namber])
            await dp.bot.send_video(chat_id=user_id, video=hist.video[day_namber])

        elif day_one:
            day_namber = 1
            day_one = False
            day_two = True
            await dp.bot.send_sticker(chat_id=user_id, sticker=hist.stick[day_namber])
            await dp.bot.send_message(chat_id=user_id, text=hist.message[day_namber])
        await asyncio.sleep(delay_in_second)


@dp.message_handler(Command('start_history'), state=None)
async def start_hist(message: types.Message, state: FSMContext):
    if await get_user_pay(message.from_user.id) == 1:
        await message.answer('Оплата не подтверждена!')
    else:
        await history(message.from_user.id)
