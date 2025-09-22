import pytest
import shutil
import os
import random
import string
from api_client import CourierClient
from config import URLS
from helpers import generate_random_string

@pytest.fixture
def create_courier():
    courier_client = CourierClient()
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }
    response = courier_client.create_courier(payload)
    yield {
        "login": login,
        "password": password,
        "response": response
    }
    login_response = courier_client.login_courier({"login": login, "password": password})
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        courier_client.delete_courier(courier_id)

def pytest_sessionstart(session):
    results_dir = "allure_results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)