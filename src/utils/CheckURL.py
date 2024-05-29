from aiogram.fsm.state import State, StatesGroup


class CheckURL(StatesGroup):
    waiting_for_url = State()
    waiting_for_date = State()
