from aiogram import types
from aiogram.types import BotCommandScopeChatAdministrators

BotCommandScopeChatAdministrators

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт бота'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('registrs', 'Регистрация'),
        types.BotCommand('submit_homework', 'Сдать домашнее задание'),
        types.BotCommand('start_history', 'Начало истории'),
    ])
