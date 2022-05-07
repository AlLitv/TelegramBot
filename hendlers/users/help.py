from aiogram import types
from loader import dp
from data import config


@dp.message_handler(text='/help')
async def command_start(message: types.Message):
    await message.answer_sticker(config.stiker_id['help_stiker'])
    await message.answer(f"Привет! Я — <b>Энди</b>, попугай из тропиков.\n"
                         f"Могу тебе чем то помочЬ?",
                         parse_mode='html')