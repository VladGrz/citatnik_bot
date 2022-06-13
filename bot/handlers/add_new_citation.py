import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from loader import dp

from data.database import add_citation

from bot.states.add_citation import AddingCitation
from bot.keyboards.add_citation_kb import add_or_cancel_adding_kb


@dp.message_handler(commands=['new'], state='*')
@dp.message_handler(CommandStart(deep_link="add"), state='*')
async def add_new_citation(message: Message):
    """
    Catching user`s desire to add new citation.
    It can be done by command `/new` or by pressing 'Додати цитату' button in
    inline menu.
    """
    await message.answer("Надішліть мені аудіо/голосовий файл.")

    # Setting state to wait for the file
    await AddingCitation.citation_file.set()


@dp.message_handler(content_types=['audio', 'voice'],
                    state=AddingCitation.citation_file)
async def file(message: Message, state: FSMContext):
    """
    Catching file if it is audio or voice
    and user is in appropriate state.
    """
    await state.update_data(file=message)

    # Setting next state to request name of the citation
    await AddingCitation.next()
    await message.answer('Напишіть мені назву, за якою розпізнаєте цитату.')


@dp.message_handler(content_types=['text'],
                    state=AddingCitation.citation_name)
async def file_name(message: Message, state: FSMContext):
    """
    Catching citation name if it is text message
    and user is in appropriate state.
    """
    name = message.text
    await state.update_data(file_name=name)
    data = await state.get_data()
    await add_citation(data['file'], data['file_name'])
    await state.finish()
    await message.answer("Успішно додав аудіоцитату",
                         reply_markup=add_or_cancel_adding_kb)


@dp.callback_query_handler(text='continue')
async def next_citation(call: CallbackQuery):
    """ Catching user`s desire to add one more citation. """
    await call.answer()
    await add_new_citation(call.message)
