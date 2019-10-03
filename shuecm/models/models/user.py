import time
import typing

import umongo
from umongo import fields

from shuecm.models.db import Instance

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
        result = await user.commit()
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
