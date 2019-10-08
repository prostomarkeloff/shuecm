import typing

from vk import types
from vk.bot_framework import NamedRule

from db.models.user import UserInChat
from db.structs.status import Permission
from shuecm.utils import levenshtein


class Texts(NamedRule):
    key = "texts"
    prefix = ["", "!", "/", "."]  # support many prefixes
    meta = {
        "name": "Texts",
        "description": "Checking message text. Using levenshtein distance for solving wrong messages",
        "deprecated": False,
    }

    __slots__ = ("texts",)

    def __init__(self, texts: typing.List[str]):  # noqa
        self.texts: typing.List[str] = []
        for text in texts:
            for prefix in self.prefix:
                self.texts.append(prefix + text.lower())

    async def check(self, message: types.Message, data: dict) -> bool:
        msg: str = message.text.lower()
        passed: bool = False
        for text in self.texts:
            ratio: float = levenshtein(text, msg)
            if ratio < 1.5:
                passed = True
                break

        return passed


class TextsWithArgs(Texts):
    key = "texts_with_args"
    meta = {
        "name": "TextsWithArgs",
        "description": "Checks message text with arguments",
        "deprecated": False,
    }

    __slots__ = ("texts",)

    # texts with args.

    def __init__(self, texts: typing.List[str]):  # noqa
        self.texts = [text.lower() for text in texts]
        vars = []  # noqa
        for text in self.texts:
            for var in self.prefix:
                vars.append(var + text)
        self.texts = vars

    async def check(self, message: types.Message, data: dict) -> bool:
        msg: str = message.text.lower()
        splitted: typing.List[str] = msg.split()
        passed: bool = False
        for text in self.texts:
            splitted_text: typing.List[str] = text.split()
            texts_length: int = len(splitted_text)
            msg_length: int = len(splitted)
            if msg_length < texts_length:
                continue
            res: typing.List[str] = splitted[0:texts_length]
            if res == splitted_text:
                passed = True
                break
        return passed


class UserHavePermission(NamedRule):
    key = "with_permissions"
    meta = {
        "name": "UserHavePermission",
        "description": "Check user permissions",
        "deprecated": False,
    }

    __slots__ = ("permissions",)

    def __init__(self, permissions: typing.List[str]):
        self.permissions: typing.List[str] = []
        for perm in permissions:
            if isinstance(perm, Permission):
                self.permissions.append(perm.value)
            else:
                self.permissions.append(perm)

    async def check(self, message: types.Message, data: dict) -> bool:
        current_user_permissions: dict = await data["current_user_in_chat"].permissions(
            data["current_user_in_chat"].get_roles()
        )  # used only in chats
        passed: bool = True
        for permission in self.permissions:
            if not current_user_permissions.get(permission, False):
                passed = False
                break
        return passed


__all__ = ["Texts", "TextsWithArgs", "UserHavePermission"]
