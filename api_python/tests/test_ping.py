# Auto‑generated tests for group: ping
# Language: python
# Framework: pytest

from tests.base_test import BaseTest
from src.api_client import APIClient

class TestPing(BaseTest):
    def test_ping_get_request(self, api_client: APIClient):
        response = api_client.get("/ping")
        assert response.status_code == 201
