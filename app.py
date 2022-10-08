from data.config import logger
async def on_startapp(dp):
    logger.info("бот запущен")
    from utils.notify_admins import on_startapp_notify
    await on_startapp_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    from loader import hist
    await hist.fill_in_data()


if __name__ == '__main__':
    try:
        from aiogram import executor
        from hendlers import dp
        executor.start_polling(dp, on_startup=on_startapp)
    except Exception as err:
        logger.exception(err)
