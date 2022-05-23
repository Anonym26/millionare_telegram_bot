import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils import executor

from config import BOT_TOKEN, admin_id

# Объект бота
bot = Bot(BOT_TOKEN, parse_mode="HTML")

# Диспетчер для бота
loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text=f"bot_started")


if __name__ == '__main__':
    # Запуск бота
    from app.handlers import dp

    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)
