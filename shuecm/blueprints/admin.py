"""
Blueprint for informational commands.
"""
from vk import types
from vk import VK
from vk.bot_framework.dispatcher import Blueprint
from vk.exceptions.errors import APIException
from vk.types.events.community.event import MessageNew

from db.structs.status import Permission
from shuecm.context import current_chat
from shuecm.utils import check_role_priority
from shuecm.utils import format_chat_id


bp = Blueprint()
api = VK.get_current().get_api()


@bp.message_handler(
    texts=["кик"], with_permissions=[Permission.CAN_KICK], with_reply_message=True
)
async def handle_kick(message: types.Message, data: dict):
    if message.reply_message.from_id == -MessageNew.get_current().group_id:
        return await message.answer(
            "⛔ Ваша роль в беседе ниже чем роль того, кого Вы пытаетесь исключить."
        )
    can_this = await check_role_priority(message.reply_message.from_id)
    if not can_this:
        return await message.answer(
            "⛔ Ваша роль в беседе ниже чем роль того, кого Вы пытаетесь исключить."
        )
    try:
        await api.messages.remove_chat_user(
            chat_id=format_chat_id(current_chat.get().chat_id),
            member_id=message.reply_message.from_id,
        )
    except APIException:
        return await message.answer("⛔ Упс.. Что-то пошло не так.")
    await message.answer("✅ Пользователь успешно удалён!")


__all__ = ["bp"]
