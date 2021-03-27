import time
import typing

import numpy as np
import xmltodict
from vk import VK

from db.models.user import User
from db.models.user import UserInChat
from shuecm.context import current_chat
from shuecm.context import current_user_in_chat


async def check_role_priority(other_user_id: int) -> bool:
    """Returns True if current user priority higher than other user"""
    if other_user_id < 0:
        return True
    user = current_user_in_chat.get()
    user_priority: int = 0
    async for role in user.get_roles():
        user_priority += role["priority"]
    other_user_priority: int = 0
    other_user_ = await User.get_user(other_user_id)
    other_user: UserInChat
    if not other_user_:
        return False
    other_user = await UserInChat.get_user(
        chat=current_chat.get().pk, user=other_user_.pk
    )

    async for role in other_user.get_roles():
        other_user_priority += role["priority"]

    return user_priority > other_user_priority


def format_chat_id(chat_id: int) -> int:
    """Format chat id for 'api.message.remove_chat_user'"""
    return chat_id - 2000000000


async def get_user_profile_text(current_user: User, in_chat: bool = False, **kwargs):
    client = VK.get_current().client
    async with client.get(f"https://vk.com/foaf.php?id={current_user.uid}") as resp:
        resp = await resp.text()
        parsed = xmltodict.parse(resp)
        vk_reg_date = (
            parsed["rdf:RDF"]["foaf:Person"]["ya:created"]["@dc:date"]
            .replace("-", ".")
            .replace("T", " | ")
            .replace("+03:00", "")
        )

    usr: User = current_user
    reg_date = time.strftime("%d.%m.%Y | %H:%M:%S", time.localtime(usr.created_time))
    if in_chat:
        usr_in_chat: UserInChat = kwargs.pop("user_in_chat")
        roles = []
        async for role in usr_in_chat.get_roles():
            roles.append(role["name"])
        roles = ", ".join(roles)
        if not roles:
            roles = "❌"
        join_date = time.strftime(
            "%d.%m.%Y | %H:%M:%S", time.localtime(usr_in_chat.join_date)
        )
        text = f"""
💭 Информация о пользователе:

🌈 ID: {usr.uid}
💤 Дата регистрации в ВК: {vk_reg_date}
💤 Дата регистрации в @shuecm: {reg_date}
⭐ Роли: {roles}
👤 Дата вступления в беседу: {join_date}
"""
    else:
        text = f"""
💭 Информация о пользователе:

🌈 ID: {usr.uid}
💤 Дата регистрации в ВК: {vk_reg_date}
💤 Дата регистрации в @shuecm: {reg_date}
👥 Состоит в: {len(usr.accounts)} беседах.
"""
    return text


def levenshtein(seq1: typing.Sequence[str], seq2: typing.Sequence[str]) -> float:
    """
    Levenshtein distance for text(s) rule.

    Author: https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
    :param seq1:
    :param seq2:
    :return: if it's similarly - returns 1.0, else - more than 1.0 ;)
    """
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1, matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1
                )
    return matrix[size_x - 1, size_y - 1]
