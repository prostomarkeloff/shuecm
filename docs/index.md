# Базовая информация

### Краткий обзор

ShueCM - Быстрый, дополняемый и расширяемый чат менеджер для Вконтакте, полностью
асинхронный и разрабатываемый заинтересованным сообществом.

### Текущий статус проекта

* [x] Самая большая скорость работы
* [x] Удобная установка
* [x] Типизация
* [x] Документация
* [x] Полная асинхронность
* [ ] Docker
* [ ] Система кастомных ролей
* [ ] Популярнее остальных ЧМ

### Использование


Установите зависимости
```sh
git clone https://github.com/shueteam/shuecm
cd shuecm
python3 -m virtualenv venv
source venv/bin/activate
pip install poetry
cd shuecm
poetry install
cd ..
mv .bot.env.example .bot.env
mv .database.env.example .database.env
mv .general.env.example .general.env
nano .bot.env # edit config
nano .database.env # edit config №2
sudo chmod +x scripts/local-run
```

Запустите чат-менеджера
```sh
./local-run
```
