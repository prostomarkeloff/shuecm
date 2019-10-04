"""
For work with user statuses.
"""
from enum import IntFlag


class Status(IntFlag):
    USER = 1  # the simply user in chat
    MODERATOR = 2
    SENIOR_MODERATOR = 3
    ADMIN = 4  # vk chat administrator
    OWNER = 5  # chat owner

    # TODO: permissions system. may be changed in user settings by admins.
