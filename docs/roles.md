# Система ролей и управление ей

### Устройство системы ролей

Система ролей подразумевает иерархию полномочий в беседе. Изначально 
чат-менеджер имеет 4 стандартных роли:

| Название        | Доступные полномочия          | 
| ------------- |:-------------:| 
| Модератор (Moderator)      | Выдача предупреждений |
| Старший модератор (SeniorModerator)      | Выдача предупреждений и исключение из беседы |
| Админ (Admin)     | Выдача предупреждений, исключение, бан |
| Владелец (Owner)      | Выдача предупреждений, выдача ролей, исключение, бан |

> Посмотреть на них устройство можно [тут](https://github.com/shueteam/shuecm/blob/master/db/structs/status.py)
 
По умолчанию есть 4 полномочия, которые в разной мере 
доступны каждой роли:

| Полномочие        | Описание            | 
| ------------- |:-------------:| 
| CAN_WRITE      | Возможность писать в чат, выдается по умолчанию всем участникам беседы | 
| CAN_WARN      | Выдача предупреждений, после определённого числа которых пользователь будет исключен      |   
| CAN_KICK| Исключение из беседы     |   
| CAN_BAN| Исключение из беседы без возможности вернуться до получения разбана      |   
|CAN_ADD_ROLES| Создание ролей прямо в беседе|

### Создание своих ролей

>**ВАЖНО: при добавлении роли с более высоким приоритетом чем у Вас, данная роль сможет Вас кикнуть, или натворить каких-либо ещё гадостей. Делайте приоритет роли владельца беседы всегда самым высоким.**

Преимущество данной системы в возможности создания **уникальных ролей**. Например
вам нужна роль, которой будет доступно только кикать, а встроенная роль
```SeniorModerator``` не подходит, ведь она может ещё и выдавать предупреждения.
 Тогда вам нужно создать свою роль младшего модератора.

```python3
from db.models.role import Role
from db.models.chat import Chat
from db.structs.status import Permission

await Role.create_role(
        chat=chat,  # информация о чате, полученная из бд
        name="JuniorModerator",  # название роли
        permissions={Permission.CAN_KICK.value: True},  # возможность кикать
```
Полномочие ```CAN_WRITE``` в словарь permissions указывать необязательно, оно выдается
всем пользователям по умолчанию.

### Ограничение использования команд по ролям

Суть создания иерархии в беседе, чтобы часть команд была ограничена
для простых юзеров. Вот пример команды, доступной только тем ролям,
которые имеют полномочие на варны *(Permission.CAN_WARN)*.

Для этого в [rules](https://github.com/shueteam/shuecm/blob/master/shuecm/rules/__init__.py)
 уже есть именованное правило **with_permissions**, воспользуемся им. Для новой
 команды я создам новый blueprint, архитектуру чат-менеджера лучше делать именно так.

```python3
from vk import types
from vk import VK
from vk.bot_framework.dispatcher import Blueprint
from db.structs.status import Permission


bp = Blueprint()
api = VK.get_current().get_api()


@bp.message_handler(
    texts=["проверка"], with_permissions=[Permission.CAN_WARN]
)
async def handle_kick(message: types.Message, data: dict):
    await message.answer("Вы можете варнить!")
```

Если пользователь с определённой ролью не должен взаимодействовать 
командами с пользователями ролью выше, воспользуйтесь функцией
**check_role_priority**. Простой [пример](https://github.com/shueteam/shuecm/blob/master/shuecm/blueprints/admin.py) уже существует в боте, это 
кик участника из беседы, логично, что модератору должно быть 
запрещено кикать старшего модератора, хотя возможность кикать у него 
должна быть.

Результат проверки кладется в переменную **can_this**.
```python3
from vk import types
from vk import VK
from vk.bot_framework.dispatcher import Blueprint

from db.structs.status import Permission
from shuecm.context import current_chat
from shuecm.utils import check_role_priority
from shuecm.utils import format_chat_id

bp = Blueprint()
api = VK.get_current().get_api()


@bp.message_handler(
    texts=["кик"], with_permissions=[Permission.CAN_KICK], with_reply_message=True
)
async def handle_kick(message: types.Message, data: dict):
    can_this = await check_role_priority(message.reply_message.from_id)
    if not can_this:
        return await message.answer(
            "Ваша роль в беседе ниже чем роль того, кого Вы пытаетесь исключить."
        )
    await api.messages.remove_chat_user(
        chat_id=format_chat_id(current_chat.get().chat_id),
        user_id=message.reply_message.from_id,
    )
    await message.answer("Пользователь успешно удалён!")
```