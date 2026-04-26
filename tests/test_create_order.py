import allure
import requests

from test_url import ORDERS_URL
from helper import get_first_ingredient_hash
from test_data import (
    SUCCESS_FIELD,
    MESSAGE_FIELD,
    ORDER_FIELD,
    NUMBER_FIELD,
    INGREDIENTS_FIELD,
    MESSAGE_INGREDIENTS_REQUIRED,
    ERROR_CREATE_ORDER_200,
    ERROR_CREATE_ORDER_400,
    ERROR_CREATE_ORDER_400_INVALID,
    AUTHORIZATION_HEADER
)


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами возвращает 200")
    @allure.description("Проверяем, что авторизованный пользователь может создать заказ с ингредиентами.")
    def test_create_order_with_auth_returns_200(self, auth_token):
        ingredient_hash = get_first_ingredient_hash()
        headers = {AUTHORIZATION_HEADER: auth_token}
        payload = {INGREDIENTS_FIELD: [ingredient_hash]}
        response = requests.post(ORDERS_URL, headers=headers, json=payload)
        assert response.status_code == 200, \
            ERROR_CREATE_ORDER_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(SUCCESS_FIELD) is True
        assert ORDER_FIELD in response_json
        assert NUMBER_FIELD in response_json[ORDER_FIELD]

    @allure.title("Создание заказа без авторизации с ингредиентами возвращает 200")
    @allure.description("Проверяем, что неавторизованный пользователь может создать заказ с ингредиентами.")
    def test_create_order_without_auth_returns_200(self):
        ingredient_hash = get_first_ingredient_hash()
        payload = {INGREDIENTS_FIELD: [ingredient_hash]}
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 200, \
            ERROR_CREATE_ORDER_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(SUCCESS_FIELD) is True

    @allure.title("Создание заказа без ингредиентов возвращает 400")
    @allure.description("Проверяем, что заказ без ингредиентов возвращает код 400.")
    def test_create_order_without_ingredients_returns_400(self, auth_token):
        headers = {AUTHORIZATION_HEADER: auth_token}
        payload = {INGREDIENTS_FIELD: []}
        response = requests.post(ORDERS_URL, headers=headers, json=payload)
        assert response.status_code == 400, \
            ERROR_CREATE_ORDER_400.format(status_code=response.status_code)
        assert MESSAGE_INGREDIENTS_REQUIRED in response.json().get(MESSAGE_FIELD, "")

    @allure.title("Создание заказа с неверным хешем ингредиента возвращает 400")
    @allure.description("Проверяем, что заказ с невалидным хешем ингредиента возвращает 400.")
    def test_create_order_with_invalid_hash_returns_400(self, auth_token):
        headers = {AUTHORIZATION_HEADER: auth_token}
        payload = {INGREDIENTS_FIELD: ["invalid_hash"]}
        response = requests.post(ORDERS_URL, headers=headers, json=payload)
        assert response.status_code == 400, \
            ERROR_CREATE_ORDER_400_INVALID.format(status_code=response.status_code)