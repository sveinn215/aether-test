import requests
import yaml

class APIClient:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        self.base_url = self.config["base_url"]
        self.headers = self.config.get("headers", {})
        self.token = None # Initialize token to None

    def set_token(self, token):
        self.token = token
        self.headers["Cookie"] = f"token={self.token}"

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy() # Use a copy to avoid modifying the original headers dict
        if self.token and "Authorization" not in headers: # Only add if not already present
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.get(url, headers=headers, params=params)
        return response

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        if self.token and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.post(url, headers=headers, data=data, json=json)
        return response

    def put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        if self.token and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.put(url, headers=headers, data=data, json=json)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        if self.token and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.delete(url, headers=headers)
        return response

    def patch(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        if self.token and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.patch(url, headers=headers, data=data, json=json)
        return response