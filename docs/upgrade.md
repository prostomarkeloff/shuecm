# Расширение чат-менеджера

Данный чат-менеджер имеет преимущество в удобстве расширения и изменения его
функционала. Для расширения вам понадобится [библиотека](https://github.com/prostomarkeloff/vk.py), на которой основан данный
ЧМ и документация к ней.

Все команды содержатся в blueprints/ и подключаются в файле app.py

```python3
def setup_blueprints():
    from shuecm.blueprints import your_blueprint

    dp.setup_blueprint(your_blueprint)
```

#### Пример добавления команды

```python3
from vk import types
from vk.bot_framework.dispatcher import Blueprint
import datetime

bp = Blueprint()


@bp.message_handler(texts=["время", "сколько времени"])
async def time_handler(message: types.Message, data: dict):
        await message.answer(f"Текущее время: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
```