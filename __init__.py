import asyncio
import logging
from bot import bot, dp
from database import init_models
from handlers import router, scheduler
import time

print("waiting database...")
time.sleep(20)
print("database awaited")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

async def main():
    await init_models()
    scheduler.scheduler.add_job(scheduler.get_data_for_message, 'interval', minutes=1)
    scheduler.scheduler.start()
    print('Расписания запущены')
    await scheduler.get_data_for_message()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())