import time
import typing

import umongo
from umongo import fields

from ..db import Instance
from ..structs.status import DEFAULT_PERMISSIONS
from .chat import Chat
from .role import Role


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

    @staticmethod
    async def add_account(usr: "User", document_id: str):
        """
        Add user account to accounts list.
        :param usr: user object
        :param document_id: document '_id' of new account
        :return:
        """
        current: dict = usr.dump()
        accounts: list = current["accounts"]
        accounts.append(document_id)
        usr.update({"accounts": accounts})
        return await usr.commit()


@instance.register
class UserInChat(umongo.Document):  # noqa
    """
    User in some chat.
    """

    user: User = fields.ReferenceField(User)  # reference to main data about user
    chat: Chat = fields.ReferenceField(Chat)  # reference to current chat
    roles = fields.ListField(fields.ObjectIdField, default=[])

    @staticmethod
    async def create_user(user: User, chat: Chat, roles_: typing.List[Role] = None):
        """
        Create user in database
        """
        if roles_ is None:
            roles = []
        else:
            roles = [role.pk for role in roles_]
        usr = UserInChat(user=user, chat=chat, roles=roles)
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

    def get_roles(self) -> typing.AsyncGenerator[dict, None]:
        """
        Get user roles; Returns a async generator.
        :return:
        """
        roles = instance.db.role.aggregate(
            [
                {"$match": {"_id": {"$in": self.roles}}},
                {"$addFields": {"_order": {"$indexOfArray": [self.roles, "$_id"]}}},
                {"$sort": {"_order": 1}},
            ]
        )
        return roles

    async def permissions(self, roles: typing.AsyncGenerator[dict, None] = None):
        """
        Get user permissions
        :return:
        """
        if roles is None:
            roles = self.get_roles()
        permissions = DEFAULT_PERMISSIONS.copy()
        async for role in roles:
            permissions.update(role["permissions"])
        return permissions

    class Meta:
        collection = instance.db.users_in_chats
