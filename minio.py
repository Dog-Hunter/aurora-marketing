from miniopy_async import Minio
from aiogram import Bot
from aiogram.types import PhotoSize
import os

MINIO_HOST = os.getenv('MINIO_HOST')
MINIO_BUCKET = os.getenv('MINIO_BUCKET')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # http for False, https for True
)

async def get_file(bot: Bot, photo: PhotoSize):
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f"{photo.file_unique_id}.jpg"

    if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
    
    await bot.download_file(file_path, f'./tmp/{file_name}')
    try:
        await client.fput_object(
            'aurora-market', file_name, f'./tmp/{file_name}')
    except Exception as e:
        print(e)
    
    # os.remove(f'./tmp/{file_name}')