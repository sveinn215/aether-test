import requests
import yaml

class APIClient:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        self.base_url = self.config["base_url"]
        self.headers = self.config.get("headers", {})

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return response

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, data=data, json=json)
        return response

    def put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, data=data, json=json)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return response

    def patch(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, headers=self.headers, data=data, json=json)
        return response