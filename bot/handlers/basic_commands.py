import asyncio

from aiogram.types import Message

from loader import bot, dp
from data.database import reg_user

from bot.extract_info import extract_user_info


@dp.message_handler(commands=['start'])
async def greeting(message: Message):
    new_user = await reg_user(message=message)
    message_text = "Привіт! Можу зробити аудіо-цитатку з твого файлу) " \
                   "Для детальної інформації як я працюю напиши /help.\n\n"
    await message.answer(
        text=message_text)

    if new_user:
        message_text = "Ах, ледь не забув. Бачу ти в нас новенький, " \
                       "за замовчуванням твої цитати приватні, якщо хочеш, " \
                       "щоб вони відображались в глобальному пошуку, " \
                       "загляни в /settings"
        await asyncio.sleep(2)
        await message.answer(
            text=message_text)

@dp.message_handler(commands=['help'])
async def help(message: Message):
    await message.answer(text="Допомога")


@dp.message_handler(commands=['commands'])
async def commands(message: Message):
    await message.answer(text='/start - початок роботи\n'
                              '/help - допомога\n'
                              '/commands - відобразити цей список\n'
                              '/new - створити нову цитату\n'
                              '/cut - обрізати медіа')
