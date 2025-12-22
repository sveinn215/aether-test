# API Testing Framework Instructions

**Note:** This guide performs all steps automatically without asking for confirmation. The only prompts you may see are when installing packages (which require your permission) or when the script needs access to a folder.

This guide provides step-by-step instructions to create a skeleton framework for API testing using Python and `pytest`.

---

## Step 1: Set Up the Project Structure

Create a project directory and organize it as follows:

```
project_root/
│
├── api_python/
│   ├── .venv/                     # Virtual environment
│   ├── src/
│   │   └── api_client.py          # API client for making requests
│   │
│   ├── tests/
│   │   ├── base_test.py           # Base test class for common setup
│   │   └── test_example.py        # Example test file
│   │
│   ├── config/
│   │   └── config.yaml            # Configuration file (e.g., base URLs, headers)
│   │
│   ├── reports/                   # Test reports
│   │
│   ├── .pytest_cache/             # Pytest cache
│   │
│   ├── requirements.txt           # Python dependencies
│   │
│   └── run_tests.py               # Script to run tests
│
└── ...
```

---

## Step 2: Create a Virtual Environment

Create a virtual environment to isolate the project dependencies:

```bash
python -m venv api_python/.venv
```

Activate the virtual environment:

- **On macOS/Linux:**
  ```bash
  source api_python/.venv/bin/activate
  ```

- **On Windows:**
  ```bash
  .\api_python\.venv\Scripts\activate
  ```

---

## Step 3: Install Dependencies

Create a `requirements.txt` file inside the `api_python` folder and add the following dependencies:

```txt
requests>=2.31.0
pytest>=7.4.0
PyYAML>=6.0.1
```

Install the dependencies:

```bash
# Install dependencies silently (no confirmation prompts)
cd api_python && pip install -r requirements.txt -q
```

---

## Step 4: Create the API Client

In `api_python/src/api_client.py`, define a reusable API client:

```python
import requests
import yaml

class APIClient:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        self.base_url = self.config["base_url"]
        self.headers = self.config.get("headers", {})

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return response

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, data=data, json=json)
        return response

    def put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, data=data, json=json)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return response

    def patch(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, headers=self.headers, data=data, json=json)
        return response
```

---

## Step 5: Configure the Project

In `api_python/config/config.yaml`, define your API configuration:

```yaml
base_url: "https://api.example.com"
headers:
  Content-Type: "application/json"
  Authorization: "Bearer your_token_here"
```

---

## Step 6: Create a Base Test Class

In `api_python/tests/base_test.py`, define a base test class for common setup:

```python
import pytest
from src.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

class BaseTest:
    def __init__(self, api_client):
        self.api_client = api_client
```

---

## Step 7: Write a Test Case

In `api_python/tests/test_example.py`, write a test case:

```python
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
```

---

## Step 8: Run Tests

Create a `run_tests.py` script inside the `api_python` folder to execute tests:

```python
import pytest

if __name__ == "__main__":
    pytest.main(["-v", "--html=reports/report.html", "--cache-dir=.pytest_cache"])
```

Run the tests:

```bash
python run_tests.py
```

---

## Step 9: Generate Reports (Optional)

Install `pytest-html` for HTML reports:

```bash
# Install pytest-html silently
pip install pytest-html -q
```

Update `run_tests.py` to include the HTML report and cache directory:

```python
pytest.main(["-v", "--html=reports/report.html", "--cache-dir=.pytest_cache"])
```

---