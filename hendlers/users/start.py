from aiogram import types
from loader import dp
from data import config



@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    await message.answer_sticker(config.stiker_id['start_stiker'])
    await message.answer(f"Привет! Давай знакомиться, я — <b>Энди</b>, настоящий попугай из тропиков.\n"
                         f" Живу в тёплом лесу солнечной Бразилии. Люблю собирать орехи и фрукты с пальм и деревьев,\n"
                         f" летать высоко над нашими тропиками и смотреть, чем занимаются остальные.\n"
                         f" А больше всего мне нравится забраться повыше на пальму и тенёчке слушать шум моря.\n"
                         f"Вводи /help и я раскажу что тебе нужно делать!",
                         parse_mode='html')
