You are a QA engineer. Write a functional test for the following API endpoint using the specified framework and language.

Endpoint: {{endpoint}}
Method: {{method}}
Description: {{description}}
Request body schema (if any): {{request_body}}
Possible responses (status codes and schemas): {{responses}}
Framework: {{framework}}
Language: {{language}}

The test should:
- Use the specified framework and language.
- Send a request to `{{base_url}}{{endpoint}}` (replace with the real base URL if needed).
- Validate the response status and basic shape of the JSON payload.
- Include appropriate assertions and comments.
- Be runnable with the respective test runner for the framework.
- Analyze the project structure to identify existing test patterns, utilities, or base classes (e.g., `BaseTest`, `api_client`).
- If utilities like `BaseTest` and `api_client` exist, ensure the test inherits from the base class and uses the API client fixture.
- If no existing utilities are found, create a standalone test case with necessary setup and teardown logic.
- Ensure the test adheres to the project's configuration and follows best practices for API testing.

Return only the code block without any extra explanation.