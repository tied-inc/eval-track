from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from prisma.client import Prisma


@asynccontextmanager
async def with_session(*args: Any, **kwargs: Any) -> AsyncGenerator[Prisma, None]:
    db = Prisma()
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

