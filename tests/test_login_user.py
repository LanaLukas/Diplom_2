import allure
import requests
from faker import Faker

from test_url import LOGIN_URL
from test_data import (
    SUCCESS_FIELD,
    MESSAGE_FIELD,
    MESSAGE_INCORRECT_CREDENTIALS,
    EMAIL_FIELD,
    PASSWORD_FIELD,
    ERROR_LOGIN_200,
    ERROR_LOGIN_401
)

fake = Faker()


class TestLoginUser:

    @allure.title("Логин под существующим пользователем возвращает 200")
    @allure.description("Проверяем, что авторизация с корректными данными возвращает код 200 и success=True.")
    def test_login_existing_user_returns_200(self, created_user):
        payload = {
            EMAIL_FIELD: created_user[EMAIL_FIELD],
            PASSWORD_FIELD: created_user[PASSWORD_FIELD]
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 200, \
            ERROR_LOGIN_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(SUCCESS_FIELD) is True

    @allure.title("Логин с неверным email возвращает 401")
    @allure.description("Проверяем, что авторизация с несуществующим email возвращает код 401.")
    def test_login_with_wrong_email_returns_401(self, created_user):
        payload = {
            EMAIL_FIELD: fake.email(),
            PASSWORD_FIELD: created_user[PASSWORD_FIELD]
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401, \
            ERROR_LOGIN_401.format(status_code=response.status_code)
        assert MESSAGE_INCORRECT_CREDENTIALS in response.json().get(MESSAGE_FIELD, "")

    @allure.title("Логин с неверным паролем возвращает 401")
    @allure.description("Проверяем, что авторизация с неверным паролем возвращает код 401.")
    def test_login_with_wrong_password_returns_401(self, created_user):
        payload = {
            EMAIL_FIELD: created_user[EMAIL_FIELD],
            PASSWORD_FIELD: fake.password()
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401, \
            ERROR_LOGIN_401.format(status_code=response.status_code)
        assert MESSAGE_INCORRECT_CREDENTIALS in response.json().get(MESSAGE_FIELD, "")