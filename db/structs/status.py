"""
For work with user statuses.
"""
from enum import Enum
from enum import IntFlag


class Permission(Enum):
    CAN_KICK = "can_kick"
    CAN_WARN = "can_warn"
    CAN_BAN = "can_ban"
    CAN_WRITE = "can_write"
    # basic permissions
    # if necessary we can append new permissions


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
}
