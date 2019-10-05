"""
Blueprint for informational commands.
"""
from vk import types
from vk.bot_framework.addons.caching import cached_handler
from vk.bot_framework.dispatcher import Blueprint
from vk.bot_framework.storages import TTLDictStorage

from db.models.user import User
from db.models.user import UserInChat
from db.structs import Status
from shuecm.validators import valid_id_in_db

bp = Blueprint()
cache = TTLDictStorage()


# TODO: Вынести хендлеры (кто я, кто ты) в отдельный blueprint.


@bp.message_handler(texts=["помощь", "инфа", "help"])
@cached_handler(storage=cache, expire=30, for_specify_user=False)
async def handler(message: types.Message, data: dict):
    users_count: int = await User.count_documents()
    answer = f"Привет! Я чат-менеджер @shuecm. \n\n\nСейчас зарегистрировано: {users_count} пользователя(ей)!"
    return await message.cached_answer(answer)


@bp.described_handler(
    description="Обработчик для получения информации о себе",
    options=["Написать 'кто я'"],
    examples=["кто я", "я кто"],
)
@bp.message_handler(texts=["кто я", "я кто"])
async def who_i_am_handler(message: types.Message, data: dict):
    if message.from_id == message.peer_id:
        usr: User = data["current_user"]
        await message.answer(f"ID: {usr.uid}.")
    else:
        usr_in_chat: UserInChat = data["current_user_in_chat"]
        usr: User = data["current_user"]
        status = Status(usr_in_chat.status).name
        await message.answer(f"ID: {usr.uid}. Статус: {status}.")


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
@bp.message_handler(texts=["кто ты", "ты кто"], have_args=(2, [valid_id_in_db]))
@bp.message_handler(texts=["кто ты", "ты кто"], with_reply_message=True)
async def who_are_you_handler(message: types.Message, data: dict):
    # TODO: Абстрагировать получение юзера в отдельный враппер, тем самым
    # упростить хендлеры.
    if message.reply_message:
        usr: User = await User.get_user(message.reply_message.from_id)
        if not usr:
            return await message.answer("Данный пользователь не зарегистрирован!")
    else:
        usr: User = data["valid_id_in_db_user"]

    if message.peer_id != message.from_id:
        usr_in_chat: UserInChat = await UserInChat.get_user(
            user=usr.pk, chat=data["current_chat"].pk
        )
        status = Status(usr_in_chat.status).name
        await message.answer(f"ID: {usr.uid}. Статус: {status}.")

    else:
        await message.answer(f"ID: {usr.uid}.")
