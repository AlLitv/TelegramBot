from aiogram import types
from loader import dp
from data import config


@dp.message_handler(content_types=['video'])
async def command_start(message: types.Message):
    #await message.answer_sticker(config.stiker_id['start_stiker'])
    await message.answer(message.text)

