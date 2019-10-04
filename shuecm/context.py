"""
Contextvars for shuecm life cycle.
"""
from contextvars import ContextVar

from pydantic import BaseModel
from vk import VK

from db.models.chat import Chat
from db.models.user import User
from db.models.user import UserInChat


class Bot(BaseModel):
    group_id: int
    access_token: str


current_user: ContextVar[User] = ContextVar("current_user")
current_chat: ContextVar[Chat] = ContextVar("current_chat")
current_user_in_chat: ContextVar[UserInChat] = ContextVar("current_user_in_chat")
current_bot: ContextVar[Bot] = ContextVar("current_bot")  # for supporting user groups


# now this not used.
def change_bot_context(bot: Bot) -> None:
    vk = VK.get_current()
    current_bot.set(bot)
    vk.access_token = bot.access_token
