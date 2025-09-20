import pytest
import allure
from helpers import generate_random_string
from data import ACCOUNT_NOT_FOUND_MESSAGE, INSUFFICIENT_DATA_LOGIN_MESSAGE
from api_client import CourierClient


class TestCourierLogin:
    courier_client = CourierClient()

    @allure.story("Успешный логин курьера")
    @allure.title('Вход с корректными данными')
    def test_courier_login_success(self, create_courier):
        with allure.step("Отправка запроса на логин курьера"):
            login_payload = {
                "login": create_courier["login"],
                "password": create_courier["password"],
            }
            response = self.courier_client.login_courier(login_payload)

        with allure.step("Проверка успешного логина курьера"):
            assert response.status_code == 200, "Неверный статус ответа"
            response_body = response.json()
            assert "id" in response_body, "ID не найден в ответе на логин"

    @allure.story('Неуспешная авторизация')
    @allure.title('Попытка входа с невалидными данными: {test_case}')
    @pytest.mark.parametrize('test_case, credentials, expected_status, expected_message', [
        ('неверный пароль',
         lambda x: {"login": x["login"], "password": generate_random_string()},
         404, ACCOUNT_NOT_FOUND_MESSAGE),
        ('неверный логин',
         lambda x: {"login": generate_random_string(), "password": x["password"]},
         404, ACCOUNT_NOT_FOUND_MESSAGE),
        ('случайные логин и пароль',
         lambda x: {"login": generate_random_string(), "password": generate_random_string()},
         404, ACCOUNT_NOT_FOUND_MESSAGE),
        ('отсутствует логин',
         lambda x: {"login": "", "password": x["password"]},
         400, INSUFFICIENT_DATA_LOGIN_MESSAGE),
        ('отсутствует пароль',
         lambda x: {"login": x["login"], "password": ""},
         400, INSUFFICIENT_DATA_LOGIN_MESSAGE)
    ])
    def test_login_negative_cases(self, create_courier, test_case, credentials, expected_status, expected_message):
        with allure.step(f'Подготовка тестовых данных для сценария: {test_case}'):
            payload = credentials(create_courier)

        with allure.step('Отправляем POST-запрос для авторизации курьера'):
            response = self.courier_client.login_courier(payload)

        with allure.step(f'Проверяем код ответа {expected_status}'):
            assert response.status_code == expected_status, \
                f"Ожидался код ответа {expected_status}, получен {response.status_code}"

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json()["message"] == expected_message, \
                f"Неожиданное сообщение об ошибке: {response.json()['message']}"
