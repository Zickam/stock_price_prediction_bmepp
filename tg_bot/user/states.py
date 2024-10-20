from aiogram.fsm.state import State, StatesGroup

class Menu(StatesGroup):
    choose_ticker = State()
