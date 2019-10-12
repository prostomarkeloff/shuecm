"""
For work with user statuses.
"""
from enum import Enum


class Permission(Enum):
    CAN_KICK = "can_kick"
    CAN_WARN = "can_warn"
    CAN_BAN = "can_ban"
    CAN_WRITE = "can_write"
    CAN_ADD_ROLES = "can_add_roles"
    CAN_GIVE_ROLES = "can_give_roles"
    # basic permissions
    # if necessary we can append new permissions


class DefaultRole(Enum):
    NAME: str
    PERMISSIONS: dict
    PRIORITY: int


DEFAULT_PERMISSIONS = {Permission.CAN_WRITE.value: True}

MODERATOR_PERMISSIONS = {Permission.CAN_WARN.value: True}
SENIOR_MODERATOR_PERMISSIONS = {
    Permission.CAN_KICK.value: True,
    Permission.CAN_WARN.value: True,
}
ADMIN_PERMISSIONS = {
    Permission.CAN_KICK.value: True,
    Permission.CAN_WARN.value: True,
    Permission.CAN_BAN.value: True,
}
OWNER_PERMISSIONS = {
    Permission.CAN_KICK.value: True,
    Permission.CAN_WARN.value: True,
    Permission.CAN_BAN.value: True,
    Permission.CAN_ADD_ROLES.value: True,
    Permission.CAN_GIVE_ROLES.value: True,
}


class Moderator(DefaultRole):
    NAME = "Модератор"
    PERMISSIONS = MODERATOR_PERMISSIONS
    PRIORITY = 2


class SeniorModerator(DefaultRole):
    NAME = "Старший модератор"
    PERMISSIONS = SENIOR_MODERATOR_PERMISSIONS
    PRIORITY = 3


class Admin(DefaultRole):
    NAME = "Админ"
    PERMISSIONS = ADMIN_PERMISSIONS
    PRIORITY = 4


class Owner(DefaultRole):
    NAME = "Владелец"
    PERMISSIONS = OWNER_PERMISSIONS
    PRIORITY = 5


DEFAULT_ROLES = [Moderator, SeniorModerator, Admin, Owner]
