import pytest
from helper import register_new_user_and_return_data, delete_user
from test_data import Fields


@pytest.fixture
def created_user():
    user_data = register_new_user_and_return_data()
    access_token = user_data[Fields.RESPONSE].json()[Fields.ACCESS_TOKEN]
    yield user_data
    delete_user(access_token)


@pytest.fixture
def auth_token(created_user):
    response = created_user[Fields.RESPONSE]
    return response.json()[Fields.ACCESS_TOKEN]