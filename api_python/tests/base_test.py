import pytest
from src.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

class BaseTest:
    def __init__(self, api_client):
        self.api_client = api_client