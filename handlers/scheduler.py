from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import bot
import database
from datetime import datetime
from sqlalchemy import select
from aiogram.types import FSInputFile

scheduler = AsyncIOScheduler()

async def get_data_for_message():
    async with database.async_session() as session:
        current_datetime = datetime.now()
        current_time = current_datetime.time().strftime('%H:%M')
        current_time = datetime.strptime(current_time, '%H:%M').time()
        current_day = current_datetime.weekday()
        print(current_time, current_day)

        timetable = await session.execute(select(database.Timetable).where(database.Timetable.time == current_time).where(database.Timetable.day == current_day))
        a = timetable.fetchall()
        if a == []:
            return
        for i in a:
            task = await session.execute(select(database.Task).where(database.Task.id == i[0].task_id))
            b = task.fetchone()
            if b[0].photo is None:
                await send_message(b[0].chat_id, b[0].text)
            else:
                ph = './tmp/' + b[0].photo + '.jpg'
                await send_message(b[0].chat_id, b[0].text, ph)


async def send_message(chat_id, text='', photo=None):
    if photo is None:
        await bot.send_message(chat_id=chat_id, text=text)
        return
    input_file = FSInputFile(photo)
    await bot.send_photo(chat_id=chat_id, photo=input_file, caption=text)