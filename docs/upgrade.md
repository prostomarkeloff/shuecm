# Расширение чат-менеджера

Данный чат-менеджер имеет преимущество в удобстве расширения и изменения его
функционала. Для расширения вам понадобится [библиотека](https://github.com/prostomarkeloff/vk.py), на которой основан данный
ЧМ и документация к ней.

Все команды содержатся в shuecm/blueprints/ и подключаются в файле app.py

```python3
def setup_blueprints():
    from shuecm.blueprints import your_blueprint  # берем наш blueprint из shuecm/blueprints

    dp.setup_blueprint(your_blueprint)  # включаем your_blueprint в работу
```

#### Добавление функционала

Эта команда даёт возможность получить от бота текущее время в беседу, если написать "время" или "сколько времени".
```python3
from vk import types
from vk.bot_framework.dispatcher import Blueprint
import datetime

bp = Blueprint()

# texts - НЕ встроенное правило библиотеки vk.py, оно
# находится в shuecm/rules/__init__.py
@bp.message_handler(texts=["время", "сколько времени"])
async def time_handler(message: types.Message, data: dict):
    await message.answer(
        f"Текущее время: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )
```

### Обработка для сообщений

Также библиотека vk.py позволяет создавать свои настройки для обработки 
событий перед попаданием их в хендлеры сообщений. Например, нужно, чтобы бот пропускал
мимо и никак не реагировал на сообщения короче 50 символов. Для этого лучше 
всего создать новый файл в shuecm/middlewares и поместить в него наш middleware.

```python3
from vk.bot_framework import BaseMiddleware
from vk.bot_framework import SkipHandler
from vk.types.events.community.event import MessageNew
from vk.utils.get_event import get_event_object


class CheckMessageMiddleware(BaseMiddleware):
    async def pre_process_event(self, event, data: dict):
        if event["type"] != "message_new":  # проверять на длину будем только новые сообщения
            return data
        event: MessageNew = get_event_object(event)  # получаем объект пришедшего события
        if len(event.object.text) < 50:
            raise SkipHandler()  # пропускаем все остальные проверки и не реагируем на сообщение
        return data 

    async def post_process_event(self) -> None:
        pass
```

Далее добавляем нашу настройку после стандартных в файле app.py в функции setup_middlewares.
```python3
def setup_middlewares():
    from shuecm.middlewares import (
        UsersRegistrationMiddleware,
        BotAdminMiddleware,
        ChatsRegistrationMiddleware,
        CheckMessageMiddleware,
    )

    dp.setup_middleware(BotAdminMiddleware())
    dp.setup_middleware(ChatsRegistrationMiddleware())
    dp.setup_middleware(UsersRegistrationMiddleware())
    dp.setup_middleware(CheckMessageMiddleware())
```

### Правила для обработки сообщений

**rules** из библиотеки vk.py позволяют сделать проверку на что-то прямо в
хендлере сообщений. Например вам нужна команда, которой сможете пользоваться 
только вы, а создавать и модифицировать кастомную роль неудобно, тогда вы 
можете сделать свою проверку. Для этого вам нужно создать файл для неё в папке
shuecm/rules. Создадим файл is_me_rule.py с объявим в нем класс IsMe

Я хочу, чтобы бот отвечал только мне, а мой id в ВК - 256460254
```python3
from vk.bot_framework import BaseRule
from vk import types


class IsMe(BaseRule):

    def __init__(self, is_me: bool):
        self.is_me: bool = is_me

    async def check(self, message: types.Message, data: dict):
        if not self.is_me and message.from_id != 256460254:
            return True
        elif not self.is_me and message.from_id == 256460254:
            return False
        elif self.is_me and message.from_id == 256460254:
            return True
        elif self.is_me and message.from_id != 256460254:
            return False
```

Далее подключим данную проверку к нужной нам команде в blueprints

```python3
from vk import types
from vk.bot_framework.addons.caching import cached_handler
from vk.bot_framework.dispatcher import Blueprint
from vk.bot_framework.storages import TTLDictStorage
from shuecm.rules.is_me_rule import IsMe
from db.models.user import User

bp = Blueprint()
cache = TTLDictStorage()


@bp.message_handler(commands=['magic', 'магия'], IsMe(True))
async def handler(message: types.Message, data: dict):
    await message.answer("Отвечаю только человеку с id 256460254")
```

Таким образом чат-менеджер будет отвечать на эту команду
 только если id будет моим, а остальное просто игнорировать.