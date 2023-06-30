from aiogram.dispatcher.filters.state import StatesGroup, State

class ManagerState(StatesGroup):
    organization = State()
    date = State()
    description = State()
    address = State()
    media = State()
