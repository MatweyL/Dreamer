import logging as logger
from asyncio import Lock

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class UnitOfWork:

    def __init__(self, db_url: str = None):
        self.engine = create_async_engine(db_url, pool_pre_ping=True)

        self.session_maker = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        self.lock = Lock()

    async def drop_all(self, model):
        try:
            async with self.session.begin() as connection:
                await connection.run_sync(model.metadata.drop_all)
        except BaseException as e:
            logger.error(f"Error: {e}")
            logger.exception(e)

    async def create_all(self, model):
        try:
            async with self.session.begin() as connection:
                await connection.run_sync(model.metadata.create_all)
        except BaseException as e:
            logger.error(f"Error: {e}")
            logger.exception(e)

    async def __aenter__(self):
        await self.lock.acquire()
        self.session = self.session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.lock.release()

    async def commit(self):
        try:
            await self.session.commit()
        except BaseException as e:
            logger.error(f"Error: {e}")
            logger.exception(e)
            await self.rollback()
            raise e

    async def rollback(self):
        try:
            await self.session.rollback()
        except BaseException as e:
            logger.error(f"Error: {e}")
            logger.exception(e)
