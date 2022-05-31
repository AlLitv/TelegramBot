from aiogram import types
from loader import dp
from data import config


@dp.message_handler(text='/help')
async def command_start(message: types.Message):
    await message.answer_sticker(config.stiker_id['help_stiker'])
    await message.answer(f"<b>Энди</b>, на связи, прием!.\n"
                         f"Для того что бы начать историю сначала нужно зарегистрироваться!\n"
                         f"Для регистрации введи /registrs! и оплати смену!\n"
                         f"После подтверждения оплаты я с тобой свяжусь!\n"
                         f"Во время истории тебе нужно будет отправить мне свои расчеты!\n"
                         f"Для этого вводи /submit_homework",
                         parse_mode='html')
