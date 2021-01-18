from aiogram.dispatcher.filters.state import StatesGroup, State


class ValidTranslation(StatesGroup):
    link = State()
    translation = State()
