"""
Registration middleware for shuecm.
"""
import logging

from vk.bot_framework import BaseMiddleware
from vk.types.events.community.event import MessageNew
from vk.utils.get_event import get_event_object

from shuecm.models.models.chat import Chat
from shuecm.models.models.user import User

logger = logging.getLogger(__name__)


class UsersRegistrationMiddleware(BaseMiddleware):
    """
    Register users in database if event == "message_new".
    """

    async def pre_process_event(self, event: dict, data: dict) -> dict:
        if event["type"] != "message_new":
            return data

        event: MessageNew = get_event_object(event)
        usr: User = await User.get_user(event.object.from_id)
        if usr:
            data["current_user"] = usr  # place the user object to data
            return data

        usr = await User.create_user(uid=event.object.from_id)
        logger.info(f"User with id ({event.object.from_id}) succesfully registered!")
        await event.object.answer(
            f"[id{event.object.from_id}| Пользователь] успешно зарегистрирован!"
        )
        data["current_user"] = usr  # place the user object to data
        return data

    async def post_process_event(self) -> None:
        pass


class ChatsRegistrationMiddleware(BaseMiddleware):
    """
    Register chats in database if event == "message_new".
    """

    async def pre_process_event(self, event: dict, data: dict) -> dict:
        if event["type"] != "message_new":
            return data

        event: MessageNew = get_event_object(event)
        if event.object.from_id == event.object.peer_id:
            return data

        chat: Chat = await Chat.get_chat(event.object.peer_id)
        if chat:
            data["current_chat"] = chat  # place the chat object to data
            return data

        chat: Chat = await Chat.create_chat(event.object.peer_id)
        logger.info(f"Chat with id ({event.object.peer_id}) succesfully registered!")
        await event.object.answer(f"Данный чат успешно зарегистрирован!")
        data["current_chat"] = chat  # place the chat object to data
        return data

    async def post_process_event(self) -> None:
        pass
