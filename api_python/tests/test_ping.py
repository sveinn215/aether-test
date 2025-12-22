# Auto‑generated tests for group: ping
# Language: python
# Framework: pytest

class TestPingEndpoint:
    """
    Test suite for the /ping endpoint.
    """

    @pytest.fixture
    def base_url(self):
        """
        Fixture to provide the base URL for the API.
        """
        return "https://restful-booker.herokuapp.com"

    def test_ping_endpoint_returns_201(self, base_url):
        """
        Test that the /ping endpoint returns a 201 status code.
        """
        # Send a GET request to the /ping endpoint
        response = requests.get(f"{base_url}/ping")

        # Assert that the response status code is 201
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

        # Assert that the response body is empty or has the expected schema
        # Since the schema is empty for 201, we just check that the response is not None
        assert response.text is not None, "Response body should not be None"
