import uuid
import allure
import pytest
import requests
from faker import Faker

from test_url import USER_URL
from test_data import Fields, Headers, ResponseMessages, AssertionErrors

fake = Faker()


class TestUpdateUser:

    @allure.title("Изменение email авторизованного пользователя возвращает 200")
    @allure.description("Проверяем, что авторизованный пользователь может изменить email.")
    def test_update_user_email_with_auth_returns_200(self, auth_token):
        new_email = f"{uuid.uuid4()}@yandex.ru"
        headers = {Headers.AUTHORIZATION: auth_token}
        payload = {Fields.EMAIL: new_email}
        response = requests.patch(USER_URL, headers=headers, json=payload)
        assert response.status_code == 200, \
            AssertionErrors.UPDATE_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(Fields.SUCCESS) is True
        assert response_json[Fields.USER][Fields.EMAIL] == new_email

    @allure.title("Изменение name авторизованного пользователя возвращает 200")
    @allure.description("Проверяем, что авторизованный пользователь может изменить name.")
    def test_update_user_name_with_auth_returns_200(self, auth_token):
        new_name = fake.first_name()
        headers = {Headers.AUTHORIZATION: auth_token}
        payload = {Fields.NAME: new_name}
        response = requests.patch(USER_URL, headers=headers, json=payload)
        assert response.status_code == 200, \
            AssertionErrors.UPDATE_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(Fields.SUCCESS) is True
        assert response_json[Fields.USER][Fields.NAME] == new_name

    @allure.title("Изменение пароля авторизованного пользователя возвращает 200")
    @allure.description("Проверяем, что авторизованный пользователь может изменить пароль.")
    def test_update_user_password_with_auth_returns_200(self, auth_token):
        new_password = fake.password()
        headers = {Headers.AUTHORIZATION: auth_token}
        payload = {Fields.PASSWORD: new_password}
        response = requests.patch(USER_URL, headers=headers, json=payload)
        assert response.status_code == 200, \
            AssertionErrors.UPDATE_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(Fields.SUCCESS) is True

    @pytest.mark.parametrize("field,value_factory,title_word", [
        (Fields.EMAIL, lambda: fake.email(), "email"),
        (Fields.NAME, lambda: fake.first_name(), "name"),
        (Fields.PASSWORD, lambda: fake.password(), "password"),
    ])
    @allure.title("Изменение {title_word} без авторизации возвращает 401")
    @allure.description("Проверяем, что без авторизации {title_word} изменить нельзя — возвращается 401.")
    def test_update_user_without_auth_returns_401(self, field, value_factory, title_word):
        payload = {field: value_factory()}
        response = requests.patch(USER_URL, json=payload)
        assert response.status_code == 401, \
            AssertionErrors.UPDATE_401.format(status_code=response.status_code)
        assert ResponseMessages.NOT_AUTHORISED in response.json().get(Fields.MESSAGE, "")