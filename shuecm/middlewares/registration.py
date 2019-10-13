"""
Registration middleware for shuecm.
"""
import logging

from pymongo import errors as pymongo_errors
from vk.bot_framework import BaseMiddleware
from vk.bot_framework import SkipHandler
from vk.types.events.community.event import MessageNew
from vk.types.responses.messages import GetConversationMembers
from vk.types.responses.messages import GetConversationMembersResponseItem
from vk.utils.get_event import get_event_object

from db.models import Chat
from db.models.role import Role
from db.models.user import User
from db.models.user import UserInChat
from db.structs.status import Admin
from db.structs.status import Owner
from shuecm.context import current_chat
from shuecm.context import current_user
from shuecm.context import current_user_in_chat

logger = logging.getLogger(__name__)


class UsersRegistrationMiddleware(BaseMiddleware):
    """
    Register users in database if event == "message_new".
    """

    meta = {
        "name": "UsersRegistrationMiddleware",
        "description": "Register users in chats",
        "deprecated": False,
    }

    __slots__ = ()

    async def pre_process_event(self, event: dict, data: dict) -> dict:
        if event["type"] != "message_new":
            return data

        event: MessageNew = get_event_object(event)
        if event.object.from_id <= 0:
            raise SkipHandler()

        usr: User = await User.get_user(event.object.from_id)
        if usr:
            data["current_user"] = usr  # place the user object to data
            current_user.set(usr)  # change context
            if event.object.from_id != event.object.peer_id:
                user_in_chat: UserInChat = await UserInChat.get_user(
                    user=usr.pk, chat=data["current_chat"].pk
                )
                if not user_in_chat:
                    user_in_chat: UserInChat = await UserInChat.create_user(
                        usr, chat=data["current_chat"]
                    )
                    await User.add_account(usr, user_in_chat.pk)  # add new account
                data["current_user_in_chat"] = user_in_chat
                current_user_in_chat.set(user_in_chat)
            return data

        usr = await User.create_user(uid=event.object.from_id)
        logger.info(f"User with id ({event.object.from_id}) succesfully registered!")
        await event.object.answer(
            f"[id{event.object.from_id}| Пользователь] успешно зарегистрирован!"
        )
        data["current_user"] = usr  # place the user object to data
        current_user.set(usr)  # change context
        if event.object.from_id != event.object.peer_id:
            user_in_chat: UserInChat = await UserInChat.get_user(
                user=usr.pk, chat=data["current_chat"].pk
            )
            if not user_in_chat:
                user_in_chat: UserInChat = await UserInChat.create_user(
                    usr, chat=data["current_chat"]
                )
                data["current_user_in_chat"] = user_in_chat
                current_user_in_chat.set(user_in_chat)
                await User.add_account(usr, user_in_chat.pk)  # add new account
        return data

    async def post_process_event(self) -> None:
        pass


class ChatsRegistrationMiddleware(BaseMiddleware):
    """
    Register chats in database if event == "message_new".
    """

    meta = {
        "name": "ChatsRegistrationMiddleware",
        "description": "Register chats in database",
        "deprecated": False,
    }
    __slots__ = ()

    async def pre_process_event(self, event: dict, data: dict) -> dict:
        if event["type"] != "message_new":
            return data

        event: MessageNew = get_event_object(event)
        if event.object.from_id == event.object.peer_id:
            return data

        chat: Chat = await Chat.get_chat(event.object.peer_id)
        if chat:
            data["current_chat"] = chat  # place the chat object to data
            current_chat.set(chat)  # change context
            return data

        # register chat
        chat: Chat = await Chat.create_chat(event.object.peer_id)
        chat_members: GetConversationMembers.response.items = data[
            "current_chat_members"
        ]
        # register chat members
        roles: dict = await Role.register_default_roles(chat)
        member: GetConversationMembersResponseItem
        for member in chat_members:
            if member.member_id <= 0:
                continue
            usr = await User.get_user(member.member_id)
            if not usr:
                try:
                    usr = await User.create_user(member.member_id)
                except pymongo_errors.DuplicateKeyError:
                    usr = await User.get_user(member.member_id)
            if member.is_owner:
                role = [roles[Owner]]
            elif member.is_admin:
                role = [roles[Admin]]
            else:
                role = None
            user_in_chat = await UserInChat.get_user(chat.pk, usr.pk)
            if not user_in_chat:
                user_in_chat = await UserInChat.create_user(
                    user=usr.pk, chat=chat.pk, roles_=role, join_date=member.join_date
                )
                await User.add_account(usr, user_in_chat.pk)  # add new account

            user_in_chat.update(
                {"join_date": member.join_date}
            )  # replace older join_date
            await user_in_chat.commit()  # commit changes

        logger.info(f"Chat with id ({event.object.peer_id}) succesfully registered!")
        await event.object.answer(f"Данный чат успешно зарегистрирован!")
        data["current_chat"] = chat  # place the chat object to data
        current_chat.set(chat)  # change context
        return data

    async def post_process_event(self) -> None:
        pass


__all__ = ["UsersRegistrationMiddleware", "ChatsRegistrationMiddleware"]
