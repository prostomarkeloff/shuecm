"""
Validators for message args.
"""
import typing

from vk import types
from vk import VK
from vk.exceptions import APIException

from db.models.role import Role
from db.models.user import User
from shuecm.context import current_chat

vk = VK.get_current()


async def valid_role_name(arg: str, message: types.Message):
    bad_answer = "Данная роль не найдена!"
    role = await Role.get_role_in_chat(chat=current_chat.get().pk, name=arg)
    if not role:
        await message.answer(bad_answer)
        return False
    return {"valid_role_name_role": role, "valid_role_name_name": arg}


async def valid_id_in_db(
    arg: str, message: types.Message
) -> typing.Union[bool, typing.Dict[str, User]]:
    """
    Check user in database via uid or screenname.
    :param arg:
    :param message:
    :return:
    """
    bad_answer = "Неверный ID пользователя или пользователь не зарегистрирован!"

    if not arg.isdigit():
        arg: str = arg.strip("[]").split("|")[0]
        try:
            arg: int = (await vk.api_request("users.get", {"user_ids": arg}))[0]["id"]
        except APIException:
            await message.answer(bad_answer)
            return False

    usr: User = await User.get_user(uid=arg)
    if not usr:
        await message.answer(bad_answer)
        return False

    return {"valid_id_in_db_user": usr}


__all__ = ["valid_id_in_db", "valid_role_name"]
