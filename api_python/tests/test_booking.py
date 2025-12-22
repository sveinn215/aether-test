# Auto‑generated tests for group: booking
# Language: python
# Framework: pytest

class TestBookingAPI:
    """Test class for the /booking endpoint."""

    @pytest.fixture
    def api_client(self):
        """Fixture to provide an API client for making requests."""
        base_url = "https://restful-booker.herokuapp.com"
        return requests.Session()

    def test_get_all_booking_ids(self, api_client):
        """
        Test to verify that the GET /booking endpoint returns a list of booking IDs.
        Validates:
        - Response status code is 200.
        - Response payload is a non-empty list of objects with 'bookingid' property.
        """
        # Send GET request to the /booking endpoint
        response = api_client.get("/booking")

        # Assert the response status code is 200
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        # Parse the JSON response
        response_data = response.json()

        # Assert the response is a non-empty list
        assert isinstance(response_data, list), "Response should be a list"
        assert len(response_data) > 0, "Response list should not be empty"

        # Assert each item in the list has the 'bookingid' property
        for item in response_data:
            assert isinstance(item, dict), "Each item in the list should be a dictionary"
            assert "bookingid" in item, "Each item should have a 'bookingid' key"
            assert isinstance(item["bookingid"], int), "'bookingid' should be an integer"

class TestCreateBooking:
    base_url = "https://restful-booker.herokuapp.com"

    def test_create_booking(self):
        # Define the request payload
        booking_data = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 1000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-01-01",
                "checkout": "2023-01-10"
            },
            "additionalneeds": "Breakfast"
        }

        # Send POST request to create a new booking
        response = requests.post(
            f"{self.base_url}/booking",
            headers={"Content-Type": "application/json"},
            data=json.dumps(booking_data)
        )

        # Validate the response status code
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        # Parse the response JSON
        response_json = response.json()

        # Validate the response schema
        assert "bookingid" in response_json, "Response should contain 'bookingid'"
        assert "booking" in response_json, "Response should contain 'booking'"

        # Validate the booking data in the response
        booking = response_json["booking"]
        assert booking["firstname"] == booking_data["firstname"], "First name mismatch"
        assert booking["lastname"] == booking_data["lastname"], "Last name mismatch"
        assert booking["totalprice"] == booking_data["totalprice"], "Total price mismatch"
        assert booking["depositpaid"] == booking_data["depositpaid"], "Deposit paid mismatch"
        assert booking["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"], "Check-in date mismatch"
        assert booking["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"], "Check-out date mismatch"
        assert booking["additionalneeds"] == booking_data["additionalneeds"], "Additional needs mismatch"

        # Validate the booking ID is an integer
        assert isinstance(response_json["bookingid"], int), "Booking ID should be an integer"

class TestGetBooking:
    """Test suite for GET /booking/{id} endpoint."""

    @pytest.fixture
    def api_client(self):
        """Fixture to provide a base URL for the API."""
        return "https://restful-booker.herokuapp.com"

    def test_get_booking_by_id(self, api_client):
        """Test retrieving a specific booking by ID."""
        # Arrange
        booking_id = 1  # Example booking ID; can be parameterized if needed
        endpoint = f"{api_client}/booking/{booking_id}"

        # Act
        response = requests.get(endpoint)

        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()

        # Validate basic JSON structure
        assert "firstname" in response_json, "Response should contain 'firstname'"
        assert "lastname" in response_json, "Response should contain 'lastname'"
        assert "totalprice" in response_json, "Response should contain 'totalprice'"
        assert "depositpaid" in response_json, "Response should contain 'depositpaid'"
        assert "bookingdates" in response_json, "Response should contain 'bookingdates'"

        # Validate nested bookingdates structure
        booking_dates = response_json["bookingdates"]
        assert "checkin" in booking_dates, "Booking dates should contain 'checkin'"
        assert "checkout" in booking_dates, "Booking dates should contain 'checkout'"

        # Validate data types (optional but recommended)
        assert isinstance(response_json["totalprice"], int), "Total price should be an integer"
        assert isinstance(response_json["depositpaid"], bool), "Deposit paid should be a boolean"

# Assuming no existing utilities like BaseTest or api_client are found,
# this is a standalone test case.

fake = Faker()

def test_update_booking():
    # Setup: Create a new booking to get a valid booking ID
    base_url = "https://restful-booker.herokuapp.com"
    auth_url = f"{base_url}/auth"
    booking_url = f"{base_url}/booking"

    # Authenticate to get a token
    auth_payload = {
        "username": "admin",
        "password": "password123"
    }
    auth_response = requests.post(auth_url, json=auth_payload)
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    # Create a new booking
    booking_payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=1000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": fake.date_this_year().isoformat(),
            "checkout": fake.date_this_year().isoformat()
        },
        "additionalneeds": fake.sentence()
    }
    create_response = requests.post(booking_url, json=booking_payload)
    assert create_response.status_code == 200
    booking_id = create_response.json()["bookingid"]

    # Test: Update the booking
    update_url = f"{base_url}/booking/{booking_id}"
    updated_booking_payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=1000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": fake.date_this_year().isoformat(),
            "checkout": fake.date_this_year().isoformat()
        },
        "additionalneeds": fake.sentence()
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }
    update_response = requests.put(update_url, json=updated_booking_payload, headers=headers)

    # Assertions
    assert update_response.status_code == 200
    response_json = update_response.json()

    # Validate the basic shape of the JSON payload
    assert "firstname" in response_json
    assert "lastname" in response_json
    assert "totalprice" in response_json
    assert "depositpaid" in response_json
    assert "bookingdates" in response_json
    assert "checkin" in response_json["bookingdates"]
    assert "checkout" in response_json["bookingdates"]
    assert "additionalneeds" in response_json

    # Validate the updated data
    assert response_json["firstname"] == updated_booking_payload["firstname"]
    assert response_json["lastname"] == updated_booking_payload["lastname"]
    assert response_json["totalprice"] == updated_booking_payload["totalprice"]
    assert response_json["depositpaid"] == updated_booking_payload["depositpaid"]
    assert response_json["bookingdates"]["checkin"] == updated_booking_payload["bookingdates"]["checkin"]
    assert response_json["bookingdates"]["checkout"] == updated_booking_payload["bookingdates"]["checkout"]
    assert response_json["additionalneeds"] == updated_booking_payload["additionalneeds"]

    # Teardown: Delete the booking (optional, depending on test isolation needs)
    delete_url = f"{base_url}/booking/{booking_id}"
    delete_response = requests.delete(delete_url, headers=headers)
    assert delete_response.status_code == 201

class TestUpdateBooking:
    base_url = "https://restful-booker.herokuapp.com"
    auth = HTTPBasicAuth("admin", "password123")  # Replace with actual credentials

    @pytest.fixture
    def create_booking(self):
        """Fixture to create a booking and return its ID for testing."""
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-01-01",
                "checkout": "2023-01-02"
            },
            "additionalneeds": "Breakfast"
        }
        response = requests.post(
            f"{self.base_url}/booking",
            json=payload,
            auth=self.auth
        )
        assert response.status_code == 200
        booking_id = response.json()["bookingid"]
        yield booking_id
        # Cleanup: Delete the booking after test
        requests.delete(
            f"{self.base_url}/booking/{booking_id}",
            auth=self.auth
        )

    def test_patch_booking(self, create_booking):
        """Test PATCH request to update a booking with partial payload."""
        booking_id = create_booking
        payload = {
            "firstname": "Jane",
            "lastname": "Smith"
        }
        response = requests.patch(
            f"{self.base_url}/booking/{booking_id}",
            json=payload,
            auth=self.auth
        )

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.headers["Content-Type"] == "application/json", "Response should be JSON"

        # Validate response structure (if any)
        # Note: The endpoint returns an empty body for 200 OK, so we only check status
        # If the response had a body, we would validate it here, e.g.:
        # response_json = response.json()
        # assert "booking" in response_json, "Response should contain 'booking' key"

# Assuming the project has a BaseTest class and api_client fixture
# If not, you can use the standalone test case below

class TestDeleteBooking:
    """Test suite for DELETE /booking/{id} endpoint."""

    @pytest.fixture
    def api_client(self):
        """Fixture to provide an authenticated API client."""
        base_url = "https://restful-booker.herokuapp.com"
        auth = HTTPBasicAuth(username="admin", password="password123")  # Replace with actual credentials
        return {"base_url": base_url, "auth": auth}

    def test_delete_booking(self, api_client):
        """Test deleting a booking successfully."""
        # Setup: Create a booking first to get a valid booking ID
        create_booking_url = f"{api_client['base_url']}/booking"
        booking_data = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-01-01",
                "checkout": "2023-01-02"
            },
            "additionalneeds": "Breakfast"
        }
        response = requests.post(create_booking_url, json=booking_data, auth=api_client["auth"])
        assert response.status_code == 200, "Failed to create a booking for deletion test"
        booking_id = response.json()["bookingid"]

        # Test: Delete the booking
        delete_url = f"{api_client['base_url']}/booking/{booking_id}"
        response = requests.delete(delete_url, auth=api_client["auth"])

        # Assertions
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        assert response.text == "", "Response body should be empty for DELETE request"

        # Verify the booking is deleted by attempting to GET it
        get_response = requests.get(delete_url, auth=api_client["auth"])
        assert get_response.status_code == 404, "Booking should not exist after deletion"

# Standalone test case (if no BaseTest or api_client fixture exists)
def test_delete_booking_standalone():
    """Standalone test for deleting a booking."""
    base_url = "https://restful-booker.herokuapp.com"
    auth = HTTPBasicAuth(username="admin", password="password123")  # Replace with actual credentials

    # Setup: Create a booking first to get a valid booking ID
    create_booking_url = f"{base_url}/booking"
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-02"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(create_booking_url, json=booking_data, auth=auth)
    assert response.status_code == 200, "Failed to create a booking for deletion test"
    booking_id = response.json()["bookingid"]

    # Test: Delete the booking
    delete_url = f"{base_url}/booking/{booking_id}"
    response = requests.delete(delete_url, auth=auth)

    # Assertions
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    assert response.text == "", "Response body should be empty for DELETE request"

    # Verify the booking is deleted by attempting to GET it
    get_response = requests.get(delete_url, auth=auth)
    assert get_response.status_code == 404, "Booking should not exist after deletion"
