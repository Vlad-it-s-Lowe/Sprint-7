import requests
from config import URLS 


class BaseApiClient:
    def __init__(self, base_url):
        self.base_url = base_url


class CourierClient(BaseApiClient):
    def __init__(self):
        super().__init__(URLS.URL_COURIER)
        self.login_url = URLS.URL_COURIER_LOGIN
    def create_courier(self, payload):
        return requests.post(self.base_url, json=payload)

    def login_courier(self, payload):
        return requests.post(self.login_url, json=payload)

    def delete_courier(self, courier_id):
        return requests.delete(f"{self.base_url}/{courier_id}")


class OrdersClient(BaseApiClient):
    def __init__(self):
        super().__init__(URLS.URL_ORDERS)

    def create_order(self, payload):
        return requests.post(self.base_url, json=payload)

    def get_orders(self, params=None):
        return requests.get(self.base_url, params=params)