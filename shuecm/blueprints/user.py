"""
Blueprint for user commands.
"""
from vk import types
from vk.bot_framework.addons.caching import cached_handler
from vk.bot_framework.dispatcher import Blueprint
from vk.bot_framework.storages import TTLDictStorage

from db.models.user import User
from db.models.user import UserInChat
from shuecm.validators import valid_id_in_db

bp = Blueprint()
cache = TTLDictStorage()


@bp.described_handler(
    description="Обработчик для получения информации о себе",
    options=["Написать 'кто я'"],
    examples=["кто я", "я кто"],
)
@bp.message_handler(texts=["кто я", "я кто"])
@cached_handler(cache, for_specify_user=True)
async def who_i_am_handler(message: types.Message, data: dict):
    if message.from_id == message.peer_id:
        usr: User = data["current_user"]
        return await message.cached_answer(f"ID: {usr.uid}.")
    else:
        usr_in_chat: UserInChat = data["current_user_in_chat"]
        usr: User = data["current_user"]
        return await message.cached_answer(f"ID: {usr.uid}.")


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
@bp.message_handler(texts_with_args=["кто ты", "ты кто"], with_reply_message=True)
@bp.message_handler(
    texts_with_args=["кто ты", "ты кто"], count_fwd_messages=1, with_fwd_messages=True
)
async def who_are_you_handler(message: types.Message, data: dict):
    if message.reply_message:
        usr: User = await User.get_user(message.reply_message.from_id)
    elif message.fwd_messages:
        usr: User = await User.get_user(message.fwd_messages[0].from_id)
    else:
        usr: User = data["valid_id_in_db_user"]

    if not usr:
        return await message.answer("Данный пользователь не зарегистрирован!")

    if message.peer_id != message.from_id:
        usr_in_chat: UserInChat = await UserInChat.get_user(
            user=usr.pk, chat=data["current_chat"].pk
        )
        await message.answer(f"ID: {usr.uid}.")

    else:
        await message.answer(f"ID: {usr.uid}.")


__all__ = ["bp"]
