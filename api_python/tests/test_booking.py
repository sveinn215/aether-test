# Auto‑generated tests for group: booking
# Language: python
# Framework: pytest

from tests.base_test import BaseTest
from src.api_client import APIClient

class TestBooking(BaseTest):
    def test_get_booking_list_all(self, api_client: APIClient):
        response = api_client.get("/booking")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        for item in response.json():
            assert isinstance(item, dict)
            assert "bookingid" in item
            assert isinstance(item["bookingid"], int)

    def test_create_booking_john_doe_old_schema(self, api_client: APIClient):
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-05"
            },
            "additionalneeds": "None"
        }
        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200
        # Add more assertions here based on the response schema

    def test_get_booking_by_id_one(self, api_client: APIClient, create_booking_id):
        booking_id = create_booking_id
        response = api_client.get(f"/booking/{booking_id}")
        assert response.status_code == 200
        # Add more assertions here based on the response schema
        # Example:
        # data = response.json()
        # assert data["id"] == booking_id

    def test_create_booking_full_payload(self, api_client: APIClient):
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-05"
            },
            "additionalneeds": "None"
        }
        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200
        # Add more assertions here based on the response schema
        # Example:
        # data = response.json()
        # assert data["firstname"] == "John"
        # assert data["lastname"] == "Doe"
        # assert data["totalprice"] == 111
        # assert data["depositpaid"] == True
        # assert data["bookingdates"]["checkin"] == "2024-01-01"
        # assert data["bookingdates"]["checkout"] == "2024-01-05"
        # assert data["additionalneeds"] == "None"

    def test_update_booking_full_payload(self, authenticated_api_client: APIClient, create_booking_id):
        booking_id = create_booking_id
        payload = {
            "firstname": "Jane",
            "lastname": "Smith",
            "totalprice": 222,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2024-02-01",
                "checkout": "2024-02-05"
            },
            "additionalneeds": "Wheelchair access"
        }
        response = authenticated_api_client.put(f"/booking/{booking_id}", json=payload)
        assert response.status_code == 200
        # Add more assertions here based on the response schema
        # Example:
        # data = response.json()
        # assert data["firstname"] == "Jane"
        # assert data["lastname"] == "Smith"
        # assert data["totalprice"] == 222
        # assert data["depositpaid"] == False
        # assert data["bookingdates"]["checkin"] == "2024-02-01"
        # assert data["bookingdates"]["checkout"] == "2024-02-05"
        # assert data["additionalneeds"] == "Wheelchair access"

    def test_delete_booking_one(self, authenticated_api_client: APIClient, create_booking_id):
        booking_id = create_booking_id
        response = authenticated_api_client.delete(f"/booking/{booking_id}")
        assert response.status_code == 201
        # No content is returned on successful deletion, so no assertions on the response body are needed.

    def test_get_booking_by_id_with_specific_fields(self, api_client: APIClient, create_booking_id):
        booking_id = create_booking_id
        response = api_client.get(f"/booking/{booking_id}")
        assert response.status_code == 200
        data = response.json()
        assert "firstname" in data
        assert "lastname" in data
        assert "totalprice" in data
        assert "depositpaid" in data
        assert "bookingdates" in data
        assert "checkin" in data["bookingdates"]
        assert "checkout" in data["bookingdates"]

    def test_create_booking_name_email_schema(self, api_client: APIClient):
        payload = {
            "firstname": "Another",
            "lastname": "Booking",
            "totalprice": 333,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2024-03-01",
                "checkout": "2024-03-05"
            },
            "additionalneeds": "Breakfast"
        }
        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "bookingid" in data
        assert "booking" in data
        assert data["booking"]["firstname"] == "Another"
        assert data["booking"]["lastname"] == "Booking"
        assert data["booking"]["totalprice"] == 333
        assert data["booking"]["depositpaid"] == False
        assert data["booking"]["bookingdates"]["checkin"] == "2024-03-01"
        assert data["booking"]["bookingdates"]["checkout"] == "2024-03-05"
        assert data["booking"]["additionalneeds"] == "Breakfast"

    def test_update_booking_name_email_schema(self, authenticated_api_client: APIClient, create_booking_id):
        booking_id = create_booking_id
        payload = {
            "firstname": "UpdatedJane",
            "lastname": "UpdatedDoe",
            "totalprice": 444,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-01",
                "checkout": "2024-04-05"
            },
            "additionalneeds": "Lunch"
        }
        response = authenticated_api_client.put(f"/booking/{booking_id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["firstname"] == "UpdatedJane"
        assert data["lastname"] == "UpdatedDoe"
        assert data["totalprice"] == 444
        assert data["depositpaid"] == True
        assert data["bookingdates"]["checkin"] == "2024-04-01"
        assert data["bookingdates"]["checkout"] == "2024-04-05"
        assert data["additionalneeds"] == "Lunch"

    def test_delete_booking_no_content_assertion(self, authenticated_api_client: APIClient, create_booking_id):
        booking_id = create_booking_id
        response = authenticated_api_client.delete(f"/booking/{booking_id}")
        assert response.status_code == 201
        assert response.text == "Created"

