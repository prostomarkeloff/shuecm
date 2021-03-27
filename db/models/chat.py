import time
import typing

import umongo
from umongo import fields

from db.db import Instance

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class Chat(umongo.Document):  # noqa
    """
    Chat document in database
    """

    chat_id = fields.IntegerField(required=True, unique=True)
    created_time = fields.IntegerField(default=time.time)

    class Meta:
        collection = instance.db.chats

    @staticmethod
    async def create_chat(chat_id: int) -> typing.Union["Chat", typing.NoReturn]:
        """
        Create chat in database or raise exception. - umongo.exceptions.UMongoError
        :param chat_id:
        :return:
        """
        chat: Chat = Chat(chat_id=chat_id)
        await chat.commit()
        return chat

    @staticmethod
    async def get_chat(chat_id: int) -> typing.Union["Chat", typing.NoReturn]:
        """
        Lookup chat in database via chat_id.
        :param chat_id:
        :return:
        """
        chat = await Chat.find_one({"chat_id": chat_id})
        return chat
