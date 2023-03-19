# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import Boolean, Column, Integer, String
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app3.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# async def get_db():
#     session = AsyncSession(engine)
#     try:
#         yield session
#     finally:
#         await session.close()




#fake db
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


