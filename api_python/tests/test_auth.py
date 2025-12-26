# Auto‑generated tests for group: auth
# Language: python
# Framework: pytest

from tests.base_test import BaseTest
from src.api_client import APIClient

class TestAuth(BaseTest):
    def test_auth_post(self, api_client: APIClient):
        payload = {
            "username": "admin",
            "password": "password123"
        }
        response = api_client.post("/auth", json=payload)
        print("Auth Response Headers:", response.headers)
        response_json = response.json()
        print("Auth Response JSON:", response_json)
        assert response.status_code == 200
        assert "token" in response_json
        api_client.set_token(response_json["token"]) # Set the obtained token