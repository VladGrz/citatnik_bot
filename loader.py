import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

# Defining basic Bot object through which we will connect to Telegram Api
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Defining storage to store info about citation in states
storage = MemoryStorage()

# Defining dispatcher which will process incoming updates
dp = Dispatcher(bot, storage=storage)
