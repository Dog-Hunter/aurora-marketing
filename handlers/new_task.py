from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from datetime import datetime, time
import handlers.states as states, handlers.kb as kb, database, re
from minio import get_file

router = Router()

@router.message(Command('new'))
async def new(message: Message, state: FSMContext):
    await state.set_state(states.NewTask.name)
    await message.answer('Введите название задачи: ')

@router.message(states.NewTask.name)
async def new_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(states.NewTask.text)
    await message.answer('Текст задачи: ')

@router.message(states.NewTask.text)
async def new_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(states.NewTask.photo)
    await message.answer('Фото: ')

@router.message(states.NewTask.photo, F.text == 'skip')
async def new_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await state.set_state(states.NewTask.chat_id)
    await message.answer('ID чата: ')

@router.message(states.NewTask.photo, F.photo)
async def new_photo(message: Message, state: FSMContext):
    await get_file(message.bot, message.photo[-1])
    await state.update_data(photo=message.photo[-1].file_unique_id)
    await state.set_state(states.NewTask.chat_id)
    await message.answer('ID чата: ')

@router.message(states.NewTask.photo)
async def new_photo(message: Message, state: FSMContext):
    await message.answer('Требуется фото или "skip"')

@router.message(states.NewTask.chat_id, lambda x: re.match('-?\d+', x.text))
async def new_chat_id(message: Message, state: FSMContext):
    await state.update_data(chat_id=int('-100' + str(abs(int(message.text)))))
    await state.set_state(states.NewTask.day)
    await message.answer('День недели: ', reply_markup=kb.day_kb)

@router.message(states.NewTask.chat_id, lambda x: not re.match('-?\d+', x.text))
async def new_chat_id_invalid(message: Message):
    await message.answer('Неправильный ID чата')

@router.callback_query(states.NewTask.day)
async def new_day(call: CallbackQuery, state: FSMContext):
    await state.update_data(day=call.data)
    await state.set_state(states.NewTask.time)
    await call.message.answer('Время в формате ЧЧ:ММ: ')

@router.message(states.NewTask.time, lambda x: not re.match(r'\d{2}:\d{2}', x.text))
async def new_time_invalid(message: Message):
    await message.answer('Неправильное время')

@router.message(states.NewTask.time)
async def new_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()
    task = database.Task(
        name=data['name'],
        text=data['text'],
        photo=data['photo'] if data['photo'] != 'skip' else None,
        chat_id=int(data['chat_id'])
    )
    async with database.async_session() as session:
        session.add(task)
        await session.commit()
        schedule_task = database.Timetable(
            day=int(data['day']),
            time=time.fromisoformat(data['time']),
            task_id=task.id,
            user_id=message.from_user.id
        )
        session.add(schedule_task)
        await session.commit()
    await state.clear()
    await message.answer('Задача добавлена')