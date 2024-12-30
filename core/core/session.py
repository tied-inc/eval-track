from contextlib import asynccontextmanager
from typing import AsyncContextManager, Any

from prisma.client import Prisma


@asynccontextmanager
async def with_session(*args: Any, **kwargs: Any) -> AsyncContextManager[Prisma]:
    db = Prisma()
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

