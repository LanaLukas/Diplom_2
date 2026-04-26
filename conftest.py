import pytest
from helper import register_new_user_and_return_data, delete_user
from test_data import ACCESS_TOKEN_FIELD, RESPONSE_FIELD


@pytest.fixture
def created_user():
    user_data = register_new_user_and_return_data()
    access_token = user_data[RESPONSE_FIELD].json()[ACCESS_TOKEN_FIELD]
    yield user_data
    delete_user(access_token)


@pytest.fixture
def auth_token(created_user):
    response = created_user[RESPONSE_FIELD]
    return response.json()[ACCESS_TOKEN_FIELD]