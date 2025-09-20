import pytest
import shutil
import os
import random
import string
from api_client import CourierClient
from config import URLS

# Функция для генерации случайной строки
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Фикстура для создания курьера
@pytest.fixture
def create_courier():
    courier_client = CourierClient()  # Создаем экземпляр API-клиента

    # генерируем данные для курьера
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    # Создание курьера
    response = courier_client.create_courier(payload)

    # Возвращаем данные курьера для использования в тесте + response
    yield {
        "login": login,
        "password": password,
        'response': response
    }

    # Удаление курьера после выполнения теста.
    login_response = courier_client.login_courier({"login": login, "password": password})
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        courier_client.delete_courier(courier_id)

# Хук для очистки allure_results
def pytest_sessionstart(session):
    """Очистка папки allure_results перед запуском тестов."""
    results_dir = "allure_results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)
