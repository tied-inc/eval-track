from prisma import Prisma
from contextlib import asynccontextmanager


@asynccontextmanager
async def with_session(*args, **kwargs):
    db = Prisma()
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

