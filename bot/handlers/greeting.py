from aiogram.types import Message

from loader import bot, dp


@dp.message_handler(commands=['start'])
async def greeting(message: Message):
    print("hi")
    await message.answer(text="Привіт! Можу зробити аудіо-цитатку з твого файлу) Для детальної інформації як я працюю напиши /help.")