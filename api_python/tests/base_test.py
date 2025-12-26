import pytest
import os
from src.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    return APIClient(config_path="api_python/config/config.yaml")

@pytest.fixture(scope="session")
def authenticated_api_client(api_client):
    # This might need to be dynamic, but for now, hardcode admin credentials
    payload = {
        "username": "admin",
        "password": "password123"
    }
    # Perform authentication
    response = api_client.post("/auth", json=payload)
    assert response.status_code == 200
    token = response.json()["token"]
    api_client.set_token(token)
    return api_client

@pytest.fixture(scope="function")
def create_booking_id(authenticated_api_client):
    payload = {
        "firstname": "Dynamic",
        "lastname": "Booking",
        "totalprice": 999,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-05-01",
            "checkout": "2024-05-05"
        },
        "additionalneeds": "Dinner"
    }
    response = authenticated_api_client.post("/booking", json=payload)
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    yield booking_id
    # Teardown: Delete the created booking
    authenticated_api_client.delete(f"/booking/{booking_id}")

class BaseTest:
    pass