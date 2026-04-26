import allure
import requests

from test_url import ORDERS_URL
from test_data import (
    SUCCESS_FIELD,
    MESSAGE_FIELD,
    ORDERS_FIELD,
    MESSAGE_NOT_AUTHORISED,
    AUTHORIZATION_HEADER,
    ERROR_GET_ORDERS_200,
    ERROR_GET_ORDERS_401
)


class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя возвращает 200")
    @allure.description("Проверяем, что авторизованный пользователь получает список своих заказов.")
    def test_get_orders_with_auth_returns_200(self, auth_token):
        headers = {AUTHORIZATION_HEADER: auth_token}
        response = requests.get(ORDERS_URL, headers=headers)
        assert response.status_code == 200, \
            ERROR_GET_ORDERS_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(SUCCESS_FIELD) is True
        assert ORDERS_FIELD in response_json

    @allure.title("Получение заказов без авторизации возвращает 401")
    @allure.description("Проверяем, что неавторизованный пользователь получает ошибку 401.")
    def test_get_orders_without_auth_returns_401(self):
        response = requests.get(ORDERS_URL)
        assert response.status_code == 401, \
            ERROR_GET_ORDERS_401.format(status_code=response.status_code)
        assert MESSAGE_NOT_AUTHORISED in response.json().get(MESSAGE_FIELD, "")