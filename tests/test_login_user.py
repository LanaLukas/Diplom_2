import allure
import requests
from faker import Faker

from test_url import LOGIN_URL
from test_data import Fields, ResponseMessages, AssertionErrors

fake = Faker()


class TestLoginUser:

    @allure.title("Логин под существующим пользователем возвращает 200")
    @allure.description("Проверяем, что авторизация с корректными данными возвращает код 200 и success=True.")
    def test_login_existing_user_returns_200(self, created_user):
        payload = {
            Fields.EMAIL: created_user[Fields.EMAIL],
            Fields.PASSWORD: created_user[Fields.PASSWORD]
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 200, \
            AssertionErrors.LOGIN_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(Fields.SUCCESS) is True

    @allure.title("Логин с неверным email возвращает 401")
    @allure.description("Проверяем, что авторизация с несуществующим email возвращает код 401.")
    def test_login_with_wrong_email_returns_401(self, created_user):
        payload = {
            Fields.EMAIL: fake.email(),
            Fields.PASSWORD: created_user[Fields.PASSWORD]
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401, \
            AssertionErrors.LOGIN_401.format(status_code=response.status_code)
        assert ResponseMessages.INCORRECT_CREDENTIALS in response.json().get(Fields.MESSAGE, "")

    @allure.title("Логин с неверным паролем возвращает 401")
    @allure.description("Проверяем, что авторизация с неверным паролем возвращает код 401.")
    def test_login_with_wrong_password_returns_401(self, created_user):
        payload = {
            Fields.EMAIL: created_user[Fields.EMAIL],
            Fields.PASSWORD: fake.password()
        }
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401, \
            AssertionErrors.LOGIN_401.format(status_code=response.status_code)
        assert ResponseMessages.INCORRECT_CREDENTIALS in response.json().get(Fields.MESSAGE, "")