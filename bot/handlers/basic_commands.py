import asyncio

from aiogram.types import Message

from loader import dp
from data.database import reg_user

from bot.extract_info import extract_user_info


@dp.message_handler(commands=['start'])
async def greeting(message: Message):
    """ Catching `/start` command. """

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
    """ Catching `/help` command. """

    message_text = (
        "Я можу зберегти ваші медіацитатки. Для початку роботи "
        "напишіть мені команду /citation далі слідуйте інструкціям."
        "\nЩоб додати цитату використовуйте команду /new."
        "\n\nДекілька слів про приватність. За замовчуванням ваші "
        "цитати приватні. \nЩо це означає? \nЦе означає, що при "
        "відображенні особистого списку цитат у групі, "
        "лише ви можете: \n     а) викликати цитату зі списку;\n"
        "     б) гортати сторінки ваших цитат.\n"
        "При цьому користувачі будуть бачити назви ваших цитат "
        "на сторінці, яку ви переглядаєте в даний час. "
        "Якщо бажаєте повної анонімності то краще обирати цитату "
        "в особистих повідомленнях з ботом і після цього "
        "переслати цитату в бажаний чат. Також ваші цитати "
        "не будуть відображатись в глобальному списку цитат."
        "\nЗмінити налаштування приватності можна в /settings."
        "\nЯкщо ваші цитати будуть неприватними то користувачі "
        "зможуть робити все зазначене вище, але вони досі "
        "не зможуть видаляти ваші цитати. ❗️ Видаляти цитати може "
        "лише їх власник❗️ Тому можете без побоювання видаляти "
        "цитати в загальних групах."
    )
    await message.answer(text=message_text)


@dp.message_handler(commands=['commands'])
async def commands(message: Message):
    """ Catching `/commands` command. """

    await message.answer(text='/start - початок роботи\n'
                              '/help - допомога\n'
                              '/settings - налаштування\n'
                              '/commands - відобразити цей список\n'
                              '/citation - викликати цитату\n'
                              '/new - створити нову цитату\n'
                              '/delete_citation - видалити цитату\n')


@dp.message_handler(commands=["?"])
async def invert(message: Message):
    message_text = message.reply_to_message.text
    en = "qwertyuiop[]asdfghjkl;'zxcvbnm,./"
    ua = "йцукенгшщзхїфівапролджєячсмитьбю."
    if message_text[0] in en:
        for i in message_text:
            try:
                message_text = message_text.replace(i, ua[en.index(i)])
            except ValueError:
                pass
    else:
        for i in message_text:
            try:
                message_text = message_text.replace(i, en[ua.index(i)])
            except ValueError:
                pass
    print(message_text)
    await message.reply_to_message.answer(message_text, reply=True)
    await message.delete()
