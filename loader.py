from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from history_message import History_data
from aiogram.contrib.middlewares.logging import LoggingMiddleware

storage = MemoryStorage()
bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
hist = History_data()




