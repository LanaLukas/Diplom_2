import uuid
import requests
import allure
from faker import Faker
from test_url import REGISTER_URL, USER_URL, INGREDIENTS_URL
from test_data import EMAIL_FIELD, PASSWORD_FIELD, NAME_FIELD, RESPONSE_FIELD, AUTHORIZATION_HEADER, DATA_FIELD

fake = Faker()


@allure.step('Создаем пользователя и возвращаем данные')
def register_new_user_and_return_data():
    email = f"{uuid.uuid4()}@yandex.ru"
    password = fake.password()
    name = fake.first_name()
    payload = {
        EMAIL_FIELD: email,
        PASSWORD_FIELD: password,
        NAME_FIELD: name
    }
    response = requests.post(REGISTER_URL, json=payload)
    return {
        EMAIL_FIELD: email,
        PASSWORD_FIELD: password,
        NAME_FIELD: name,
        RESPONSE_FIELD: response
    }


@allure.step('Удаляем пользователя')
def delete_user(access_token):
    headers = {AUTHORIZATION_HEADER: access_token}
    requests.delete(USER_URL, headers=headers)


@allure.step('Получаем первый ингредиент из списка')
def get_first_ingredient_hash():
    response = requests.get(INGREDIENTS_URL)
    ingredients = response.json()[DATA_FIELD]
    return ingredients[0]["_id"]