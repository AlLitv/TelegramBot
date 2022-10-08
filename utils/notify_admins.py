from data.config import logger

from aiogram import Dispatcher


from data.config import admin_id




async def on_startapp_notify(dp: Dispatcher):
    for admin in admin_id:
        try:
            text = "Bot running"
            logger.info(text)
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as er:
            logger.exception(er)

