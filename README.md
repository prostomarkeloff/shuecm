<h1 align="center">ShueCM</h1>
<p align="center">
<img src="https://img.shields.io/badge/python-3.6%2B-blue">
<a href="https://shueteam.github.io/shuecm/"><img src="https://img.shields.io/badge/-%20%20%20Docs-blue"></a>
<a href="https://github.com/shueteam/shuecm/blob/master/LICENSE"><img src="https://img.shields.io/github/license/SevereCloud/vksdk.svg?maxAge=2592000"></a>
<a href="https://vk.com/shuecm"><img src="https://img.shields.io/badge/chat-manager-%234a76a8.svg?logo=VK&logoColor=white"></a>
<img src="https://img.shields.io/badge/%D0%A8%D0%A3%D0%95-%D0%9F%D0%9F%D0%A8-red">
</p>

#### Чат-менеджер нового поколения для [Вконтакте](https://vk.com/)

> Первый чат-менеджер с полностью **открытым исходным кодом**.


### О проекте

Данный проект призван составить конкуренцию современным крупным чат-менеджерам, при этом, оставляя, весь код открытым и развивающимся за счёт заинтересованного сообщества. Одна из главных целей - **скорость**, поэтому ЧМ основан на самой
быстрой из существующих библиотек для взаимодействия с API Вконтакте - [vk.py](https://github.com/prostomarkeloff/vk.py), а в качестве базы данных используется [MongoDB](https://github.com/Scille/umongo).


### Преимущества

- Высокая скорость работы
- Открытое [API](https://github.com/shueteam/shuecm/tree/master/api) (в активной разработке)
- Максимально возможная типизация кода
- Всеобъемлющая [документация](https://shueteam.github.io/shuecm/)
- Бесплатное использование всеми желающими
- Возможно использование как общего [Чат-Менеджера](https://vk.com/shuecm), так и установка его в свою группу
- Настройка системы ролей для управления ЧМ
- Удобная адаптация ЧМ под свои нужды
    - Команды
    - Реакции на события
- [Приложение](https://github.com/shueteam/shuecm-vk-mini-apps) Вконтакте для удобства использования


### Установка для личного использования

```sh
git clone https://github.com/shueteam/shuecm
cd shuecm
python3 -m virtualenv venv
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
./local-run
# Enjoy!
```
Скоро и для Docker!

### Вклад в развитие

Проект нуждается в вашей помощи, любые вопросы получат ответ, а предложения будут приняты к сведению.
