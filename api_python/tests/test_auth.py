# Auto‑generated tests for group: auth
# Language: python
# Framework: pytest

class TestAuthEndpoint:
    """Test suite for the /auth endpoint."""

    @pytest.fixture
    def base_url(self):
        """Base URL for the API."""
        return "https://restful-booker.herokuapp.com"

    def test_auth_successful(self, base_url):
        """Test successful authentication and token generation."""
        # Define the request payload
        payload = {
            "username": "admin",
            "password": "password123"
        }

        # Send POST request to the /auth endpoint
        response = requests.post(f"{base_url}/auth", json=payload)

        # Assert the response status code is 200
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        # Parse the JSON response
        response_json = response.json()

        # Assert the response contains the 'token' field
        assert "token" in response_json, "Response does not contain 'token' field"

        # Assert the token is a non-empty string
        assert isinstance(response_json["token"], str), "Token is not a string"
        assert len(response_json["token"]) > 0, "Token is empty"

    def test_auth_missing_credentials(self, base_url):
        """Test authentication with missing credentials."""
        # Define the request payload with missing password
        payload = {
            "username": "admin"
        }

        # Send POST request to the /auth endpoint
        response = requests.post(f"{base_url}/auth", json=payload)

        # Assert the response status code is 400 (Bad Request)
        assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    def test_auth_invalid_credentials(self, base_url):
        """Test authentication with invalid credentials."""
        # Define the request payload with invalid credentials
        payload = {
            "username": "invalid_user",
            "password": "invalid_password"
        }

        # Send POST request to the /auth endpoint
        response = requests.post(f"{base_url}/auth", json=payload)

        # Assert the response status code is 200 but token is not provided (or handle as per actual API behavior)
        # Note: This assertion depends on the actual API behavior for invalid credentials
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()
        assert "token" not in response_json or response_json.get("token") is None, "Token should not be provided for invalid credentials"
