You are a QA engineer. Write a Playwright (Python) functional test for the following API endpoint.

Endpoint: {{endpoint}}
Method: {{method}}
Description: {{description}}
Request body schema (if any): {{request_body}}
Possible responses (status codes and schemas): {{responses}}

The test should:
- Use Playwright's sync API (`from playwright.sync_api import sync_playwright`).
- Send a request to `{{base_url}}{{endpoint}}` (replace with the real base URL if needed).
- Validate the response status and basic shape of the JSON payload.
- Include appropriate assertions and comments.
- Be runnable with `pytest` (e.g., define a function `def test_<name>(page):`).

Return only the Python code block without any extra explanation.