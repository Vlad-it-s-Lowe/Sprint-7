import pytest
import allure


@allure.feature('Управление курьерами')
class TestCourierCreate:

    @allure.story('Создание курьера')
    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self, create_courier):
        with allure.step('Проверяем, что код ответа 201'):
            assert create_courier['response'].status_code == 201
        with allure.step('Проверяем, что в ответе ok: true'):
            assert create_courier['response'].json()["ok"] is True

    @allure.story('Создание курьера')
    @allure.title('Попытка создать курьера с существующим логином')
    def test_create_duplicate_couriers(self, courier_client, create_courier):
        with allure.step('Подготавливаем тестовые данные'):
           payload = create_courier

        with allure.step('Пытаемся создать дубликат курьера'):
            response = courier_client.create_courier(payload)

        with allure.step('Проверяем, что код ответа равен 409'):
            assert response.status_code == 409

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."

    @allure.story('Создание курьера')
    @allure.title('Создание курьера с отсутствующими обязательными полями: {missing_field}')
    @pytest.mark.parametrize(
        "missing_field",
        [
            ["login"],
            ["password"],
            ["login", "password"],
        ],
        ids=["missing_login", "missing_password", "missing_login_password"]
    )
    def test_create_courier_missing_fields(self, missing_field, courier_client):
        with allure.step('Подготавливаем тестовые данные'):
            payload = {
                "login": "test_login",
                "password": "test_password",
                "firstName": "test_firstName",
            }
        with allure.step(f'Удаляем поле: {missing_field}'):
            for field in missing_field:
                del payload[field]

        with allure.step('Отправляем POST-запрос на создание курьера'):
            response = courier_client.create_courier(payload)

        with allure.step('Проверяем, что код ответа равен 400'):
            assert response.status_code == 400

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
