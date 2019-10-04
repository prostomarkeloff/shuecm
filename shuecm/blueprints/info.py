"""
Blueprint for informational commands.
"""
from vk import types
from vk.bot_framework.dispatcher import Blueprint

from db.models.user import User

bp = Blueprint()


@bp.message_handler(text="инфа")
async def info_handler(message: types.Message, data: dict):
    await message.answer("Тестовое сообщение!")


@bp.message_handler(text="кто я")
async def who_i_am_handler(message: types.Message, data: dict):
    usr: User = data["current_user"]
    await message.answer(
        f"ID: {usr.uid}\n Дата регистрации: {usr.created_time} секунд с 01.01.1970"
    )
