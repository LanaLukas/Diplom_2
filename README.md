# Diplom_2

API тесты для сервиса Stellar Burgers.


Установить зависимости - `pip install -r requirements.txt`

Запуск тестов - `pytest -v`

Сгенерировать allure отчёт - `pytest -v --alluredir=allure_results`

Открыть отчёт - `allure serve allure_results`
___

Документация API: https://code.s3.yandex.net/qa-automation-engineer/python-full/diploma/api-Stelar_Burger_10.25.pdf?etag=3584917d935c90b69cb3ffaff58d4f34

Проверяемые ручки:

- `POST /api/auth/register` - создание пользователя
- `POST /api/auth/login` - авторизация пользователя
- `PATCH /api/auth/user` - обновление данных пользователя
- `POST /api/orders` - создание заказа
- `GET /api/orders` - получение заказов пользователя
