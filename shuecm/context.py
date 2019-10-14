"""
Contextvars for shuecm life cycle.
"""
from contextvars import ContextVar

from db.models.chat import Chat
from db.models.user import User
from db.models.user import UserInChat

# it will be set in middlewares, may be in args validators.
current_user: ContextVar[User] = ContextVar("current_user")
current_chat: ContextVar[Chat] = ContextVar("current_chat")
current_user_in_chat: ContextVar[UserInChat] = ContextVar("current_user_in_chat")

__all__ = ["current_user", "current_chat", "current_user_in_chat"]
