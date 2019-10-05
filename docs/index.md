# Базовая информация

### Краткий обзор

ShueCM - Быстрый, дополняемый и расширяемый чат менеджер для Вконтакте, полностью
асинхронный и разрабатываемый заинтересованным сообществом.

### Текущий статус проекта

- Самая большая скорость работы - :white_check_mark:
- Удобная установка - :white_check_mark:
- Типизация - :white_check_mark:
- Документация - :white_check_mark:
- Полная асинхронность - :white_check_mark:
- Docker - :clock3:
- Система кастомных ролей - :clock3:
- Популярнее остальных ЧМ - :clock3:

### Деплой

Склонируйте репозиторий
```sh
git clone https://github.com/shueteam/shuecm
cd shuecm
```

Установите зависимости
```sh
pip install poetry
poetry install
pre-commit install
```
Создайте текстовый файл .env и поместите в него значения, указанные
в .env.example
```sh
VK_TOKEN="123"
VK_GROUP_ID="123"

# mongodb settings
MONGODB_CONNECTION_URI="123"
MONGODB_DATABASE_NAME="test"

# Sentry settings
SENTRY_DSN=""

# logging settings
LOGGING_LEVEL="INFO"

# global settings
PRODUCTION=false
```
Запустите чат-менеджера
```sh
python3 shuecm/app.py
```