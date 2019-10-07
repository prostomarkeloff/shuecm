import logging

from vk import VK
from vk.bot_framework import BaseMiddleware
from vk.bot_framework import SkipHandler
from vk.exceptions import APIException
from vk.types.events.community.event import MessageNew
from vk.types.message import Action
from vk.types.responses.messages import GetConversationMembers
from vk.utils.get_event import get_event_object

logger = logging.getLogger(__name__)


class BotAdminMiddleware(BaseMiddleware):
    meta = {
        "name": "BotAdminMiddleware",
        "description": "Checks if bot is admin",
        "deprecated": False,
    }
    __slots__ = ("api",)

    def __init__(self):
        super().__init__()
        self.api = VK.get_current(no_error=False).get_api()

    async def pre_process_event(self, event: dict, data: dict) -> dict:
        if event["type"] != "message_new":
            return data

        event: MessageNew = get_event_object(event)
        if event.object.peer_id == event.object.from_id:
            return data
        if event.object.action:
            if event.object.action.type is Action.chat_invite_user.value:
                message = (
                    "Привет, я @shuecm! Исходный код проекта -- https://github.com/shueteam/shuecm. Для корректной "
                    "работы бота, ему нужны права администратора. "
                )
                if event.object.action.member_id == -event.group_id:
                    await event.object.answer(message)
                    return data

        try:
            result: GetConversationMembers = (
                await self.api.messages.get_conversation_members(
                    peer_id=event.object.peer_id
                )
            )
            data[
                "current_chat_members"
            ] = result.response.items  # place the chat members to data
            return data
        except APIException:
            await event.object.answer(
                "Бот не может работать без прав администратора в беседе!"
            )
            raise SkipHandler()

    async def post_process_event(self) -> None:
        pass


__all__ = ["BotAdminMiddleware"]
