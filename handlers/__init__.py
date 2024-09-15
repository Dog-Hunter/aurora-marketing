from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import handlers.new_task as new_task
import database

router = Router()
router.include_router(new_task.router)

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    try:
        user = database.User(
            telegram_id=message.from_user.id,
            username=message.from_user.full_name
        )
        async with database.async_session() as session:
            session.add(user)
            await session.commit()
    except Exception as e:
        pass
    await message.answer("Привет!\nЯ помогу тебе вести расписание отправки сообщений.\n")

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(str(message.chat.id))