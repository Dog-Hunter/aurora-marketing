from sqlalchemy import Column, Integer, BigInteger, String, Time, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String)

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    photo = Column(String, nullable=True)
    chat_id = Column(BigInteger)

class Timetable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True)
    task_id = Column(BigInteger, ForeignKey('task.id'))
    user_id = Column(BigInteger, ForeignKey('user.telegram_id'))
    day = Column(Integer)
    time = Column(Time)

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)