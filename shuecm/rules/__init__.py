import typing

from vk import types
from vk.bot_framework import NamedRule

from db.structs.status import Permission
from shuecm.utils import levenshtein


class TextsWithArgs(NamedRule):
    key = "texts_with_args"
    prefix = ["", "!", "/", "."]  # support many prefixes
    meta = {
        "name": "TextsWithArgs",
        "description": "Check message text (args supported)",
        "deprecated": False,
    }

    # texts with args.

    def __init__(self, texts: typing.List[str]):
        self.texts = [text.lower() for text in texts]
        vars = []  # noqa
        for text in self.texts:
            for var in self.prefix:
                vars.append(var + text)
        self.texts = vars

    async def check(self, message: types.Message, data: dict):
        msg = message.text.lower()
        splitted = msg.split()
        passed = False
        for text in self.texts:
            splitted_text = text.split()
            texts_lenght = len(splitted_text)
            msg_lenght = len(splitted)
            if msg_lenght < texts_lenght:
                continue
            res = splitted[0:texts_lenght]
            if res == splitted_text:
                passed = True
                break
        return passed


class Texts(NamedRule):
    key = "texts"
    prefix = ["", "!", "/", "."]  # support many prefixes
    meta = {"name": "Texts", "description": "Check message text", "deprecated": False}

    # texts with args.

    def __init__(self, texts: typing.List[str]):
        self.texts = [text.lower() for text in texts]
        vars = []  # noqa
        for text in self.texts:
            for var in self.prefix:
                vars.append(var + text)
        self.texts = vars

    async def check(self, message: types.Message, data: dict):
        msg = message.text.lower()
        passed = False
        for text in self.texts:
            ratio = levenshtein(text, msg)
            print(ratio)
            if ratio < 1.5:
                passed = True
                break

        return passed


class UserHavePermission(NamedRule):
    key = "with_permissions"

    def __init__(self, permissions: typing.List[str]):
        self.permissions: typing.List[str] = []
        for perm in permissions:
            if isinstance(perm, Permission):
                self.permissions.append(perm.name)
            else:
                self.permissions.append(perm)

    async def check(self, message: types.Message, data: dict):
        current_user_permissions = data[
            "current_user_in_chat"
        ].dump()  # used only in chats
        passed: bool = True
        for permission in self.permissions:
            res = permission in current_user_permissions["permissions"]
            if not res:
                passed = False
                break
        return passed
