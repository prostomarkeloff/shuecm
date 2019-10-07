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

#### Пример добавления команды

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
