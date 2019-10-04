"""
Ensure indexes, etc.
"""
import asyncio

from .models.chat import Chat
from .models.user import User
from .models.user import UserInChat


async def populate_db(drop_db: bool = False):
    if drop_db:
        await User.collection.drop()
        await UserInChat.collection.drop()
        await Chat.collection.drop()
    await User.ensure_indexes()
    await UserInChat.ensure_indexes()
    await Chat.ensure_indexes()


def pre_start(loop: asyncio.AbstractEventLoop, drop_db: bool = False):
    loop.create_task(populate_db(drop_db))
