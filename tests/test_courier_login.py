import pytest
import allure


class TestCourierLogin:

    @allure.story("Успешный логин курьера")
    @allure.title('Вход с корректными данными')
    def test_courier_login_success(self, create_courier, courier_client):
        with allure.step("Отправка запроса на логин курьера"):
            login_payload = {
                "login": create_courier["login"],
                "password": create_courier["password"],
            }
            response = courier_client.login_courier(login_payload)

        with allure.step("Проверка успешного логина курьера"):
            assert response.status_code == 200, "Неверный статус ответа"
            response_body = response.json()
            assert "id" in response_body, "ID не найден в ответе на логин"

    @allure.story('Неуспешная авторизация')
    @allure.title('Попытка входа с невалидными данными: {test_case}')
    @pytest.mark.parametrize('test_case, credentials, expected_status, expected_message', [
        ('неверный пароль',
         lambda x: {"login": x["login"], "password": "invalid_password"},
         404, "Не учетная запись не найдена"),
        ('неверный логин',
         lambda x: {"login": "invalid_login", "password": x["password"]},
         404, "Не учетная запись не найдена"),
        ('случайные логин и пароль',
         lambda x: {"login": "invalid_login", "password": "invalid_password"},
         404, "Не учетная запись не найдена"),
        ('отсутствует логин',
         lambda x: {"login": "", "password": x["password"]},
         400, "Недостаточно данных для входа"),
        ('отсутствует пароль',
         lambda x: {"login": x["login"], "password": ""},
         400, "Недостаточно данных для входа")
    ])
    def test_login_negative_cases(self, create_courier, test_case, credentials, expected_status, expected_message, courier_client):
        with allure.step(f'Подготовка тестовых данных для сценария: {test_case}'):
            payload = credentials(create_courier)

        with allure.step('Отправляем POST-запрос для авторизации курьера'):
            response = courier_client.login_courier(payload)

        with allure.step(f'Проверяем код ответа {expected_status}'):
            assert response.status_code == expected_status, \
                f"Ожидался код ответа {expected_status}, получен {response.status_code}"

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json()["message"] == expected_message, \
                f"Неожиданное сообщение об ошибке: {response.json()['message']}"