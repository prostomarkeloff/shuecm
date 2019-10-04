"""
Ensure indexes, etc.
"""
import asyncio

from .models.user import User


async def populate_db(drop_db: bool = False):
    if drop_db:
        await User.collection.drop()
    await User.ensure_indexes()


def pre_start(loop: asyncio.AbstractEventLoop, drop_db: bool = False):
    loop.create_task(populate_db(drop_db))
