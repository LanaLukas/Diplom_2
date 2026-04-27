import uuid
import requests
import allure
from faker import Faker
from test_url import REGISTER_URL, USER_URL, INGREDIENTS_URL
from test_data import Fields, Headers

fake = Faker()


def generate_create_unique_user_payload():
    return {
        Fields.EMAIL: f"{uuid.uuid4()}@yandex.ru",
        Fields.PASSWORD: fake.password(),
        Fields.NAME: fake.first_name()
    }


@allure.step('Создаем пользователя и возвращаем данные')
def register_new_user_and_return_data():
    payload = generate_create_unique_user_payload()
    response = requests.post(REGISTER_URL, json=payload)
    return {Fields.RESPONSE: response, **payload}


@allure.step('Удаляем пользователя')
def delete_user(access_token):
    headers = {Headers.AUTHORIZATION: access_token}
    requests.delete(USER_URL, headers=headers)


@allure.step('Получаем первый ингредиент из списка')
def get_first_ingredient_hash():
    response = requests.get(INGREDIENTS_URL)
    ingredients = response.json()[Fields.DATA]
    return ingredients[0]["_id"]