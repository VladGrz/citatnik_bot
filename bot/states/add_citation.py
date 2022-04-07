from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingCitation(StatesGroup):
    citation_file = State()
    citation_name = State()

