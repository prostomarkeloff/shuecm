"""
Blueprint for work with roles.
"""
import typing

from vk import types
from vk.bot_framework.addons.caching import cached_handler
from vk.bot_framework.dispatcher import Blueprint
from vk.bot_framework.storages import TTLDictStorage

from db.models.role import Role
from db.models.user import User
from db.models.user import UserInChat
from db.structs.status import Permission
from shuecm.validators import valid_role_name_in_db

bp = Blueprint()
cache = TTLDictStorage()


@bp.message_handler(texts=["роли"], in_chat=True)
@cached_handler(cache, expire=10, for_specify_user=True)
async def chat_roles(message: types.Message, data: dict):
    roles = await Role.get_roles_in_chat(chat=data["current_chat"].pk)
    text = "📗 Текущие роли в беседе: \n\n"
    for role in sorted(roles, key=lambda role: role.priority, reverse=True):
        text += f"✏ Название: {role.name}.\n ⭐ Приоритет: {role.priority}.\n ℹ Полномочия: {', '.join(role.permissions)}\n\n"

    return await message.cached_answer(text)


@bp.described_handler(
    description="Обработчик для выдачи роли пользователю.",
    have_args=["Имя роли в БД"],
    examples=["выдать роль <имя_роли> *пересланное сообщение*"],
)
@bp.message_handler(
    texts_with_args=["выдать роль"],
    in_chat=True,
    have_args=(2, [valid_role_name_in_db]),
    with_reply_message=True,
    with_permissions=[Permission.CAN_GIVE_ROLES],
)
async def give_role(message: types.Message, data: dict):
    role = data["valid_role_name_in_db_role"]
    usr = await User.get_user(message.reply_message.from_id)
    if not usr:
        return await message.answer("⛔ Данный пользователь не зарегистрирован!")
    usr_in_chat = await UserInChat.get_user(chat=data["current_chat"].pk, user=usr.pk)
    have_this_role = False
    async for role_ in usr_in_chat.get_roles():
        if role_["name"] == data["valid_role_name_in_db_name"]:
            have_this_role = True
            break

    if have_this_role:
        return await message.answer("⛔ У данного пользователя уже есть эта роль!")
    await UserInChat.add_role(user=usr_in_chat, role=role.pk)
    await message.answer("✅ Данная роль успешно выдана пользователю!")


@bp.described_handler(
    description="Обработчик для добавления роли для беседы",
    have_args=["Имя роли", "Приоритет", "Возможности"],
)
@bp.message_handler(
    texts_with_args=["добавить роль", "создать роль"],
    in_chat=True,
    with_permissions=[Permission.CAN_ADD_ROLES],
)
async def add_role(message: types.Message, data: dict):
    args = message.get_args()[1:]  # first arg it's 'роль' word
    if len(args) < 3:
        return
    name: str
    priority: typing.Union[str, int]
    permissions: typing.Union[str, typing.List[str], typing.Dict]
    name, priority, *permissions = args
    if not name.isalpha():
        return await message.answer("⛔ Некорректное имя роли!")
    if not priority.isdigit():
        return await message.answer("⛔ Некорректный приоритет роли!")
    else:
        priority = int(priority)

    if isinstance(permissions, str):
        try:
            permissions = {Permission(permissions).value: True}
        except ValueError:
            return await message.answer("⛔ Некорректный тип полномочия!")
    elif isinstance(permissions, list):
        permissions_ = {}
        perm: str
        for perm in permissions:
            perm = perm.lower().strip(",")
            try:
                perm_ = Permission(perm)
            except ValueError:
                return await message.answer("⛔ Некорректный тип полномочия!")
            permissions_[perm_.value] = True
        permissions = permissions_

    res = await Role.get_role_in_chat(chat=data["current_chat"].pk, name=name)
    if res:
        return await message.answer("⛔ Роль с указанным именем уже существует!")
    await Role.create_role(
        chat=data["current_chat"], name=name, priority=priority, permissions=permissions
    )
    await message.answer("✅ Роль успешно создана!")


__all__ = ["bp"]
