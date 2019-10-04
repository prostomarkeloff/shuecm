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
    User document in database
    """

    uid = fields.IntegerField(required=True, unique=True)
    created_time = fields.IntegerField(default=time.time)

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


@instance.register
class UserInChat(umongo.Document):  # noqa

    chat = fields.ReferenceField(Chat)  # reference to current chat
    status = fields.IntegerField(
        default=1
    )  # status of user. will be converted to `db.structs.Status`

    class Meta:
        collection = instance.db.users_in_chats
