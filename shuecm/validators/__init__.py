"""
Validators for message args.
"""
import typing

from vk import types
from vk import VK
from vk.exceptions import APIException

from db.models.user import User

vk = VK.get_current()


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


__all__ = ["valid_id_in_db"]
