import typing

from vk import types
from vk.bot_framework import NamedRule


class Texts(NamedRule):
    key = "texts"
    meta = {"name": "Texts", "description": "Check message text", "deprecated": False}

    # texts with args.

    def __init__(self, texts: typing.List[str]):
        self.texts = [text.lower() for text in texts]

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
