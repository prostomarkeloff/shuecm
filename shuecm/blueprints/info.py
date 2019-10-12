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
    answer = f"Привет! Я чат-менеджер @shuecm. \n\n\nСейчас зарегистрировано: {users_count} пользователя(ей)!"
    return await message.cached_answer(answer)


@bp.message_handler(texts=["роли"])
async def info_role_handler(message: types.Message, data: dict):
    text = (
        "Подробнее о ролях: https://shueteam.github.io/shuecm/roles/.\n\n ВАЖНО: при добавлении роли с более "
        "высоким приоритетом чем у Вас, данная роль сможет Вас кикнуть, или натворить каких-либо ещё гадостей. "
        "Делайте приоритет роли владельца беседы всегда самым высоким. "
    )

    await message.answer(text)


__all__ = ["bp"]
