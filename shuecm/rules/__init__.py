import typing

from vk import types
from vk.bot_framework import NamedRule


class Texts(NamedRule):
    key = "texts"
    meta = {"name": "Texts", "description": "Check message text", "deprecated": False}

    def __init__(self, texts: typing.List[str]):
        self.texts = [text.lower() for text in texts]

    async def check(self, message: types.Message, data: dict):
        return message.text.lower() in self.texts
