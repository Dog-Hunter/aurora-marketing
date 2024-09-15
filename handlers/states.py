from aiogram.fsm.state import State, StatesGroup


class NewTask(StatesGroup):
    name = State()
    text = State()
    photo = State()
    chat_id = State()
    day = State()
    time = State()