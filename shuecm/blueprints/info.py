"""
Blueprint for informational commands.
"""
from vk import types
from vk.bot_framework.dispatcher import Blueprint

from db.models.user import User
from shuecm.validators import valid_id_in_db

bp = Blueprint()


@bp.message_handler(text="инфа")
async def info_handler(message: types.Message, data: dict):
    await message.answer("Тестовое сообщение!")


@bp.message_handler(texts=["кто я", "я кто"])
async def who_i_am_handler(message: types.Message, data: dict):
    usr: User = data["current_user"]
    await message.answer(
        f"ID: {usr.uid}\n Дата регистрации: {usr.created_time} секунд с 01.01.1970"
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
