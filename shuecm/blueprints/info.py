"""
Blueprint for informational commands.
"""
from vk import types
from vk.bot_framework.addons.caching import cached_handler
from vk.bot_framework.dispatcher import Blueprint
from vk.bot_framework.storages import TTLDictStorage

from db.models.user import User

bp = Blueprint()
cache = TTLDictStorage()


@bp.message_handler(texts=["помощь", "инфа", "help"])
@cached_handler(storage=cache, expire=30, for_specify_user=False)
async def handler(message: types.Message, data: dict):
    users_count: int = await User.count_documents()
    answer = f"📢 Привет! Я чат-менеджер @shuecm. \n\n\nСейчас зарегистрировано: {users_count} пользователя(ей)!"
    return await message.cached_answer(answer)


__all__ = ["bp"]
