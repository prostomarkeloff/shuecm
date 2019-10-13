"""
Blueprint for user commands.
"""
import time

import xmltodict
from vk import types
from vk import VK
from vk.bot_framework.addons.caching import cached_handler
from vk.bot_framework.dispatcher import Blueprint
from vk.bot_framework.storages import TTLDictStorage

from db.models.user import User
from db.models.user import UserInChat
from shuecm.validators import valid_id_in_db

bp = Blueprint()
cache = TTLDictStorage()
client = VK.get_current().client


async def get_data_about_user(current_user: User, in_chat: bool = False, **kwargs):
    async with client.get(f"https://vk.com/foaf.php?id={current_user.uid}") as resp:
        resp = await resp.text()
        parsed = xmltodict.parse(resp)
        vk_reg_date = (
            parsed["rdf:RDF"]["foaf:Person"]["ya:created"]["@dc:date"]
            .replace("-", ".")
            .replace("T", " | ")
            .replace("+03:00", "")
        )

    usr: User = current_user
    reg_date = time.strftime("%d.%m.%Y | %H:%M:%S", time.localtime(usr.created_time))
    if in_chat:
        usr_in_chat: UserInChat = kwargs.pop("user_in_chat")
        roles = []
        async for role in usr_in_chat.get_roles():
            roles.append(role["name"])
        roles = ", ".join(roles)
        if not roles:
            roles = "❌"
        join_date = time.strftime(
            "%d.%m.%Y | %H:%M:%S", time.localtime(usr_in_chat.join_date)
        )
        text = f"""
💭 Информация о пользователе:

🌈 ID: {usr.uid}
💤 Дата регистрации в ВК: {vk_reg_date}
💤 Дата регистрации в @shuecm: {reg_date}
⭐ Роли: {roles}
👤 Дата вступления в беседу: {join_date}
"""
    else:
        text = f"""
💭 Информация о пользователе:

🌈 ID: {usr.uid}
💤 Дата регистрации в ВК: {vk_reg_date}
💤 Дата регистрации в @shuecm: {reg_date}
👥 Состоит в: {len(usr.accounts)} беседах.
"""
    return text


@bp.described_handler(
    description="Обработчик для получения информации о себе",
    options=["Написать 'кто я'"],
    examples=["кто я", "я кто"],
)
@bp.message_handler(texts=["кто я", "я кто"])
@cached_handler(cache, for_specify_user=True)
async def who_i_am_handler(message: types.Message, data: dict):
    usr: User = data["current_user"]
    if message.from_id == message.peer_id:
        return await message.cached_answer(
            await get_data_about_user(usr, in_chat=False)
        )
    else:
        usr_in_chat: UserInChat = data["current_user_in_chat"]
        return await message.cached_answer(
            await get_data_about_user(usr, in_chat=True, user_in_chat=usr_in_chat)
        )


@bp.described_handler(
    description="Обработчик для получения информации о пользователе.",
    have_args=["ID пользователя, его упоминание или screenname."],
    options=[
        "Переслать сообщение пользователя, о котором нужна информация",
        "Отправить ID пользователя, его упоминание, или screenname",
    ],  # options of use case this handler
    examples=[
        "кто ты *пересланное сообщение*",
        "кто ты @durov",
        "кто ты id1",
        "кто ты durov",
    ],
)
@bp.message_handler(
    texts_with_args=["кто ты", "ты кто"], have_args=(2, [valid_id_in_db])
)
@bp.message_handler(texts=["кто ты", "ты кто"], with_reply_message=True)
@bp.message_handler(
    texts=["кто ты", "ты кто"], count_fwd_messages=1, with_fwd_messages=True
)
async def who_are_you_handler(message: types.Message, data: dict):
    if message.reply_message:
        usr: User = await User.get_user(message.reply_message.from_id)
    elif message.fwd_messages:
        usr: User = await User.get_user(message.fwd_messages[0].from_id)
    else:
        usr: User = data["valid_id_in_db_user"]

    if not usr:
        return await message.answer("⛔ Данный пользователь не зарегистрирован!")

    if message.peer_id != message.from_id:
        usr_in_chat: UserInChat = await UserInChat.get_user(
            user=usr.pk, chat=data["current_chat"].pk
        )
        await message.answer(
            await get_data_about_user(usr, in_chat=True, user_in_chat=usr_in_chat)
        )
    else:
        await message.answer(await get_data_about_user(usr, in_chat=False))


__all__ = ["bp"]
