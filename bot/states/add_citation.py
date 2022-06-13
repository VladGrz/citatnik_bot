from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingCitation(StatesGroup):
    """ Class with states to add citation. """
    # state which will wait a file from user
    citation_file = State()
    # state which will wait name for a citation
    citation_name = State()

