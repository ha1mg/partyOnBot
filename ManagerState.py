from aiogram.dispatcher.filters.state import StatesGroup, State

class ManagerState(StatesGroup):
    organization = State()
    date = State()
    description = State()
    address = State()
    media = State()
    edit_organization = State()
    edit_date = State()
    edit_description = State()
    edit_address = State()
    edit_media = State()
