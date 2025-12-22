from tests.base_test import BaseTest

class TestExample(BaseTest):
    def test_get_data(self, api_client):
        response = api_client.get("/data")
        assert response.status_code == 200
        assert "expected_data" in response.json()

    def test_post_data(self, api_client):
        payload = {"key": "value"}
        response = api_client.post("/data", json=payload)
        assert response.status_code == 201