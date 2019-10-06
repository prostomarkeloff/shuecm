import time
import typing

import umongo
from umongo import fields

from ..structs.status import DEFAULT_ROLES
from .chat import Chat
from db.db import Instance

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class Role(umongo.Document):
    """
    Custom role
    """

    name = fields.StringField(required=True)
    chat = fields.ReferenceField(Chat, required=True)
    permissions = fields.DictField(default={})

    class Meta:
        collection = instance.db.roles

    @staticmethod
    async def create_role(
        chat: Chat, name: str = ":sparkles:", permissions: dict = None
    ):
        """
        Create role in database
        :param chat:
        :param name: visible name
        :param permissions:
        :return:
        """
        if permissions is None:
            permissions = {}
        role = Role(chat=chat, name=name, permissions=permissions)
        await role.commit()
        return role

    @staticmethod
    async def register_default_roles(chat: Chat):
        roles = {}
        for role in DEFAULT_ROLES:
            role = Role(
                chat=chat, name=role.NAME.value, permissions=role.PERMISSIONS.value
            )
            role.commit()
            roles[role] = role
        return roles