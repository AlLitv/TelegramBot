from aiogram import types
from loader import dp
from data import config


@dp.message_handler(text='/help')
async def command_start(message: types.Message):
    await message.answer_sticker(config.stiker_id['help_stiker'])
    await message.answer(f"Привет! Я — <b>Энди</b>, попугай из тропиков.\n"
                         f"Для того что бы начать историю сначала нужно зарегистрироваться!\n"
                         f"Для регистрации введи /registrs!\n"
                         f"После этого введи /start_history что бы начать иисторию!\n"
                         f"Во время истории тебе нужно будет отправить мне сво расчеты!\n"
                         f"Для этого введи /submit_homework",
                         parse_mode='html')
