import time
import typing

import umongo
from umongo import fields

from .chat import Chat
from db.db import Instance

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class User(umongo.Document):  # noqa
    """
    Main user document in database
    """

    uid = fields.IntegerField(required=True, unique=True)
    created_time = fields.IntegerField(default=time.time)
    accounts = fields.ListField(
        fields.ReferenceField("UserInChat"), default=[]
    )  # accounts it is a list of

    # chats (references to chats) where user exists.

    class Meta:
        collection = instance.db.users

    @staticmethod
    async def create_user(uid: int) -> typing.Union["User", typing.NoReturn]:
        """
        Create user in database or raise exception. - umongo.exceptions.UMongoError
        :param uid:
        :return:
        """
        user: User = User(uid=uid)
        await user.commit()
        return user

    @staticmethod
    async def get_user(uid: int) -> typing.Union["User", typing.NoReturn]:
        """
        Lookup user in database via UID.
        :param uid:
        :return:
        """
        user = await User.find_one({"uid": uid})
        return user

    @staticmethod
    async def get_account(document_id: str):
        """
        Lookup user in user chats via document `_id`
        :param document_id:
        :return:
        """
        user = await User.find_one({"accounts": document_id})
        return user


@instance.register
class UserInChat(umongo.Document):  # noqa
    """
    User in something chat.
    """

    user = fields.ReferenceField(User)  # reference to main data about user
    chat = fields.ReferenceField(Chat)  # reference to current chat
    status = fields.IntegerField(
        default=1
    )  # status of user. will be converted to `db.structs.Status`

    permissions = fields.DictField(
        default={}
    )  # a user permissions. not implemented now.
    # TODO: impelement. reference to `db.structs.status`

    @staticmethod
    async def create_user(user: User, chat: Chat, status: int = 1):
        """
        Create user in database
        """
        usr = UserInChat(user=user, chat=chat, status=status)
        await usr.commit()
        return usr

    @staticmethod
    async def get_user(chat: str, user: str):
        """
        Get user via chat '_id' and user '_id'
        :param chat: _id of chat
        :param user: _id of user
        :return:
        """
        usr = await UserInChat.find_one({"chat": chat, "user": user})
        return usr

    class Meta:
        collection = instance.db.users_in_chats
