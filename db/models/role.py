import umongo
from umongo import fields

from ..structs.status import DEFAULT_ROLES
from .chat import Chat
from db.db import Instance

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class Role(umongo.Document):  # noqa
    """
    Custom role
    """

    name = fields.StringField(required=True)
    chat = fields.ReferenceField(Chat, required=True)
    permissions = fields.DictField(default={})

    priority = fields.IntegerField(required=True)

    class Meta:
        collection = instance.db.roles

    @staticmethod
    async def create_role(
        chat: Chat,
        name: str = ":sparkles:",
        permissions: dict = None,
        priority: int = 1,
    ):
        """
        Create role in database
        :param priority:
        :param chat:
        :param name: visible name
        :param permissions:
        :return:
        """
        if permissions is None:
            permissions = {}
        role = Role(chat=chat, name=name, permissions=permissions, priority=priority)
        await role.commit()
        return role

    @staticmethod
    async def register_default_roles(chat: Chat):
        roles = {}
        for role_ in DEFAULT_ROLES:
            role = Role(
                chat=chat,
                name=role_.NAME.value,
                permissions=role_.PERMISSIONS.value,
                priority=role_.PRIORITY.value,
            )
            await role.commit()
            roles[role_] = role
        return roles
