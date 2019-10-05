"""
For work with user statuses.
"""
from enum import Enum
from enum import IntFlag


class Status(IntFlag):
    USER = 1  # the simply user in chat
    MODERATOR = 2
    SENIOR_MODERATOR = 3
    ADMIN = 4  # vk chat administrator
    OWNER = 5  # chat owner


class Permission(Enum):
    CAN_KICK = "can_kick"
    CAN_WARN = "can_warn"
    CAN_BAN = "can_ban"
    # basic permissions
    # if necessary we can append new permissions


USER_PERMISSIONS = {}
MODERATOR_PERMISSIONS = {Permission.CAN_WARN.name: Permission.CAN_WARN.value}
SENIOR_MODERATOR_PERMISSIONS = {
    Permission.CAN_KICK.name: Permission.CAN_KICK.value,
    Permission.CAN_WARN.name: Permission.CAN_WARN.value,
}
ADMIN_PERMISSIONS = {
    Permission.CAN_KICK.name: Permission.CAN_KICK.value,
    Permission.CAN_WARN.name: Permission.CAN_WARN.value,
    Permission.CAN_BAN.name: Permission.CAN_BAN.value,
}
OWNER_PERMISSIONS = {
    Permission.CAN_KICK.name: Permission.CAN_KICK.value,
    Permission.CAN_WARN.name: Permission.CAN_WARN.value,
    Permission.CAN_BAN.name: Permission.CAN_BAN.value,
}
