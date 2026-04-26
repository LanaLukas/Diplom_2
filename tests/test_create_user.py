import allure
import requests
from faker import Faker

from test_url import REGISTER_URL
from test_data import (
    SUCCESS_FIELD,
    MESSAGE_FIELD,
    USER_FIELD,
    EMAIL_FIELD,
    NAME_FIELD,
    PASSWORD_FIELD,
    RESPONSE_FIELD,
    MESSAGE_USER_EXISTS,
    MESSAGE_REQUIRED_FIELDS,
    ERROR_CREATE_USER_200,
    ERROR_CREATE_USER_403
)

fake = Faker()


class TestCreateUser:

    @allure.title("Создание уникального пользователя возвращает 200")
    @allure.description("Проверяем, что при создании уникального пользователя возвращается код 200 и success=True.")
    def test_create_unique_user_returns_200(self, created_user):
        response = created_user[RESPONSE_FIELD]
        assert response.status_code == 200, \
            ERROR_CREATE_USER_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(SUCCESS_FIELD) is True
        assert USER_FIELD in response_json
        assert EMAIL_FIELD in response_json[USER_FIELD]
        assert NAME_FIELD in response_json[USER_FIELD]

    @allure.title("Создание уже зарегистрированного пользователя возвращает 403")
    @allure.description("Проверяем, что при повторной регистрации возвращается код 403 и сообщение 'User already exists'.")
    def test_create_duplicate_user_returns_403(self, created_user):
        payload = {
            EMAIL_FIELD: created_user[EMAIL_FIELD],
            PASSWORD_FIELD: created_user[PASSWORD_FIELD],
            NAME_FIELD: created_user[NAME_FIELD]
        }
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            ERROR_CREATE_USER_403.format(status_code=response.status_code)
        assert MESSAGE_USER_EXISTS in response.json().get(MESSAGE_FIELD, "")

    @allure.title("Создание пользователя без email возвращает 403")
    @allure.description("Проверяем, что при отсутствии поля email возвращается код 403.")
    def test_create_user_without_email_returns_403(self):
        payload = {PASSWORD_FIELD: fake.password(), NAME_FIELD: fake.first_name()}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            ERROR_CREATE_USER_403.format(status_code=response.status_code)
        assert MESSAGE_REQUIRED_FIELDS in response.json().get(MESSAGE_FIELD, "")

    @allure.title("Создание пользователя без password возвращает 403")
    @allure.description("Проверяем, что при отсутствии поля password возвращается код 403.")
    def test_create_user_without_password_returns_403(self):
        payload = {EMAIL_FIELD: fake.email(), NAME_FIELD: fake.first_name()}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            ERROR_CREATE_USER_403.format(status_code=response.status_code)
        assert MESSAGE_REQUIRED_FIELDS in response.json().get(MESSAGE_FIELD, "")

    @allure.title("Создание пользователя без name возвращает 403")
    @allure.description("Проверяем, что при отсутствии поля name возвращается код 403.")
    def test_create_user_without_name_returns_403(self):
        payload = {EMAIL_FIELD: fake.email(), PASSWORD_FIELD: fake.password()}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            ERROR_CREATE_USER_403.format(status_code=response.status_code)
        assert MESSAGE_REQUIRED_FIELDS in response.json().get(MESSAGE_FIELD, "")