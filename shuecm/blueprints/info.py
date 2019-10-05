"""
Blueprint for informational commands.
"""
from vk import types
from vk.bot_framework.dispatcher import Blueprint

from db.models.user import User
from db.models.user import UserInChat
from db.structs import Status
from db.structs.status import Permission
from shuecm.validators import valid_id_in_db

bp = Blueprint()


@bp.message_handler(text="привет", with_permissions=[Permission.CAN_KICK])
async def test_handler(message: types.Message, data: dict):
    # сделано исключительно для тестирования.
    await message.answer("Привет!")


@bp.described_handler(
    description="Обработчик для получения информации о себе",
    options=["Написать 'кто я'"],
    examples=["кто я", "я кто"],
)
@bp.message_handler(texts=["кто я", "я кто"])
async def who_i_am_handler(message: types.Message, data: dict):
    if message.from_id == message.peer_id:
        usr: User = data["current_user"]
        await message.answer(
            f"ID: {usr.uid}\n Дата регистрации: {usr.created_time} секунд с 01.01.1970"
        )
    else:
        usr_in_chat: UserInChat = data["current_user_in_chat"]
        usr: User = data["current_user"]
        status = Status(usr_in_chat.status).name
        await message.answer(f"ID: {usr.uid}. Статус: {status}")


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
    if message.reply_message:
        usr: User = await User.get_user(message.reply_message.from_id)
        if not usr:
            await message.answer("Данный пользователь не зарегистрирован!")
    else:
        usr: User = data["valid_id_in_db_user"]
    await message.answer(
        f"ID: {usr.uid}\n Дата регистрации: {usr.created_time} секунд с 01.01.1970"
    )
