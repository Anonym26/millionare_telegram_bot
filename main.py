import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import BOT_TOKEN, admin_id
from database import UsersCRUD

# Объект бота
bot = Bot(BOT_TOKEN, parse_mode="HTML")

# Диспетчер для бота
loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# создаем объект для работы с БД
users_db = UsersCRUD()


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Не флуди...")


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text=f"bot_started")


async def send_to_admin_shd(dp):
    """Закрывает соединение с БД и выводит сообщение"""
    users_db.close()
    await bot.send_message(chat_id=admin_id, text=f"bot_stoped")


if __name__ == '__main__':
    # Запуск бота
    from app.handlers.commands import dp

    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=send_to_admin_shd, skip_updates=True)
    import app.handlers
