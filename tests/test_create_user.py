import allure
import requests
from faker import Faker

from test_url import REGISTER_URL
from helper import generate_create_unique_user_payload
from test_data import Fields, ResponseMessages, AssertionErrors

fake = Faker()


class TestCreateUser:

    @allure.title("Создание уникального пользователя возвращает 200")
    @allure.description("Проверяем, что при создании уникального пользователя возвращается код 200 и success=True.")
    def test_create_unique_user_returns_200(self):
        payload = generate_create_unique_user_payload()
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 200, \
            AssertionErrors.CREATE_USER_200.format(status_code=response.status_code)
        response_json = response.json()
        assert response_json.get(Fields.SUCCESS) is True
        assert Fields.USER in response_json
        assert Fields.EMAIL in response_json[Fields.USER]
        assert Fields.NAME in response_json[Fields.USER]

    @allure.title("Создание уже зарегистрированного пользователя возвращает 403")
    @allure.description("Проверяем, что при повторной регистрации возвращается код 403 и сообщение 'User already exists'.")
    def test_create_duplicate_user_returns_403(self, created_user):
        payload = {
            Fields.EMAIL: created_user[Fields.EMAIL],
            Fields.PASSWORD: created_user[Fields.PASSWORD],
            Fields.NAME: created_user[Fields.NAME]
        }
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            AssertionErrors.CREATE_USER_403.format(status_code=response.status_code)
        assert ResponseMessages.USER_EXISTS in response.json().get(Fields.MESSAGE, "")

    @allure.title("Создание пользователя без email возвращает 403")
    @allure.description("Проверяем, что при отсутствии поля email возвращается код 403.")
    def test_create_user_without_email_returns_403(self):
        payload = {Fields.PASSWORD: fake.password(), Fields.NAME: fake.first_name()}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            AssertionErrors.CREATE_USER_403.format(status_code=response.status_code)
        assert ResponseMessages.REQUIRED_FIELDS in response.json().get(Fields.MESSAGE, "")

    @allure.title("Создание пользователя без password возвращает 403")
    @allure.description("Проверяем, что при отсутствии поля password возвращается код 403.")
    def test_create_user_without_password_returns_403(self):
        payload = {Fields.EMAIL: fake.email(), Fields.NAME: fake.first_name()}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            AssertionErrors.CREATE_USER_403.format(status_code=response.status_code)
        assert ResponseMessages.REQUIRED_FIELDS in response.json().get(Fields.MESSAGE, "")

    @allure.title("Создание пользователя без name возвращает 403")
    @allure.description("Проверяем, что при отсутствии поля name возвращается код 403.")
    def test_create_user_without_name_returns_403(self):
        payload = {Fields.EMAIL: fake.email(), Fields.PASSWORD: fake.password()}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403, \
            AssertionErrors.CREATE_USER_403.format(status_code=response.status_code)
        assert ResponseMessages.REQUIRED_FIELDS in response.json().get(Fields.MESSAGE, "")