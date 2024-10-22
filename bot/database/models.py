from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm._orm_constructors import mapped_column
from sqlalchemy import BigInteger, Integer, String, Boolean, JSON, LargeBinary
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from bot.config import __DATABASE__

import bot.logging.colors as colors
import bot.logging.logging as logging

log = logging.logging(Name='DB', Color=colors.yellow)

engine = create_async_engine(url=__DATABASE__)
async_session = async_sessionmaker(autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    user_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(256), nullable=True)
    first_name: Mapped[str] = mapped_column(String(256), nullable=True)
    last_name: Mapped[str] = mapped_column(String(256), nullable=True)
    send_notifications: Mapped[bool] = mapped_column(Boolean(create_constraint=True))


class Lesson(Base):
    __tablename__ = 'Lessons'

    lesson_id: Mapped[str] = mapped_column(String(256), primary_key=True)
    homework: Mapped[str] = mapped_column(String(256), nullable=True)
    photo: Mapped[bool] = mapped_column(Boolean(create_constraint=False))
    url: Mapped[str] = mapped_column(String(256), nullable=True)


class NetSchool(Base):
    __tablename__ = 'NetSchool'

    user_id = mapped_column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    enc_login: Mapped[str] = mapped_column(String(4096))
    enc_password: Mapped[str] = mapped_column(String(4096))
    enc_key: Mapped[str] = mapped_column(String(4096))


class NetSchoolData(Base):
    __tablename__ = 'NetSchoolData'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(BigInteger, unique=True)
    dairy_data = mapped_column(JSON)


async def init_db():
    log.init('Connecting to db')
    async with engine.begin() as conn:
        log.init('Creating tables')
        await conn.run_sync(Base.metadata.create_all)
