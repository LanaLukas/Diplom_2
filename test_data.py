class Fields:
    RESPONSE = "response"
    SUCCESS = "success"
    MESSAGE = "message"
    USER = "user"
    EMAIL = "email"
    PASSWORD = "password"
    NAME = "name"
    ORDER = "order"
    NUMBER = "number"
    ORDERS = "orders"
    DATA = "data"
    INGREDIENTS = "ingredients"
    ACCESS_TOKEN = "accessToken"


class Headers:
    AUTHORIZATION = "Authorization"


class ResponseMessages:
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS = "email or password are incorrect"
    NOT_AUTHORISED = "You should be authorised"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"


class AssertionErrors:
    CREATE_USER_200 = "Ожидался код 200 при создании пользователя, получен {status_code}"
    CREATE_USER_403 = "Ожидался код 403, получен {status_code}"
    LOGIN_200 = "Ожидался код 200 при логине, получен {status_code}"
    LOGIN_401 = "Ожидался код 401, получен {status_code}"
    UPDATE_200 = "Ожидался код 200 при обновлении данных, получен {status_code}"
    UPDATE_401 = "Ожидался код 401 без авторизации, получен {status_code}"
    CREATE_ORDER_200 = "Ожидался код 200 при создании заказа, получен {status_code}"
    CREATE_ORDER_400 = "Ожидался код 400 без ингредиентов, получен {status_code}"
    CREATE_ORDER_400_INVALID = "Ожидался код 400 при невалидном хеше, получен {status_code}"
    GET_ORDERS_200 = "Ожидался код 200 при получении заказов, получен {status_code}"
    GET_ORDERS_401 = "Ожидался код 401 без авторизации, получен {status_code}"