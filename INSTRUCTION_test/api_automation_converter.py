from openai import AsyncOpenAI   # <-- async client
import sys
import json
import yaml
import asyncio
import time
import argparse
from pathlib import Path
import os

# ---------- Configuration ----------
def get_spec_path() -> Path:
    """Parse command‑line arguments to obtain the OpenAPI spec file path.

    If no argument is provided, defaults to ``api_specs.yaml`` in the current
    working directory.
    """
    parser = argparse.ArgumentParser(description="Generate tests from an OpenAPI spec.")
    parser.add_argument(
        "spec_file",
        nargs="?",
        default="api_specs.yaml",
        help="Path to the OpenAPI specification file (YAML or JSON).",
    )
    args = parser.parse_args()
    return Path(args.spec_file)

api_specs_path = get_spec_path()          # change to your spec file (JSON or YAML)
# output_dir will be determined dynamically based on the detected language
instruction_path = Path("INSTRUCTION_test/api_automation_instruction.md")   # external prompt file
max_concurrency = 8                            # tune based on your hardware / Ollama limits
# -----------------------------------

def detect_language_and_framework():
    """Detect the programming language and framework from the api_* folder structure."""
    # Get all items in current directory that start with "api_"
    all_items = os.listdir(".")
    api_folders = []
    
    for item in all_items:
        if item.startswith("api_") and os.path.isdir(item):
            api_folders.append(item)
    
    if not api_folders:
        return "python", "requests"  # Default to Python and requests
    
    language = api_folders[0].replace("api_", "")
    framework = "requests"  # Default framework for Python
    
    # Detect framework based on requirements.txt or other indicators
    requirements_path = os.path.join(api_folders[0], "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r") as f:
            requirements_content = f.read()
            if "playwright" in requirements_content:
                framework = "playwright"
            elif "pytest" in requirements_content:
                framework = "pytest"
    
    return language, framework

language, framework = detect_language_and_framework()

# Determine the correct output directory based on the detected language
# Tests will be saved in the appropriate api_[language]/tests/ folder
api_folder = f"api_{language}"
tests_folder = Path(api_folder) / "tests"

# Check if the expected test folder exists, if not search for common test folder patterns
def find_test_folder():
    """Search for test folders in common locations if the expected structure doesn't exist."""
    # First check if the expected folder exists
    if tests_folder.exists():
        return tests_folder
    
    # Search for common test folder patterns
    common_test_folders = [
        "tests",
        "test",
        "spec",
        "specs",
        "test_suite",
        "testing"
    ]
    
    # Search in the api folder first
    api_path = Path(api_folder)
    if api_path.exists():
        for test_dir in common_test_folders:
            potential_folder = api_path / test_dir
            if potential_folder.exists():
                print(f"Found test folder at: {potential_folder}")
                return potential_folder
    
    # Search in the root directory
    for test_dir in common_test_folders:
        potential_folder = Path(test_dir)
        if potential_folder.exists():
            print(f"Found test folder at: {potential_folder}")
            return potential_folder
    
    # If no existing test folder found, create the default one
    print(f"No existing test folder found, creating default at: {tests_folder}")
    return tests_folder

# Use the found or created test folder
output_dir = find_test_folder()
output_dir.mkdir(parents=True, exist_ok=True)

# Load the instruction template once
try:
    instruction_template = instruction_path.read_text(encoding="utf-8")
except Exception as exc:
    print(f"Failed to read instruction file '{instruction_path}': {exc}", file=sys.stderr)
    sys.exit(1)

# Load OpenAPI spec (JSON or YAML)
def load_spec(path: Path):
    try:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(path.read_text())
        elif path.suffix.lower() == ".json":
            return json.loads(path.read_text())
        else:
            raise ValueError("Unsupported spec file type.")
    except Exception as exc:
        print(f"Failed to load spec: {exc}", file=sys.stderr)
        sys.exit(1)


def get_base_url(spec: dict) -> str:
    """Extract the base URL from the OpenAPI spec, prioritizing staging servers."""
    servers = spec.get("servers", [])
    if not servers:
        return "http://localhost:3000"  # Default fallback
    
    # Prioritize staging server if available
    for server in servers:
        server_url = server.get("url", "")
        if "staging" in server_url.lower():
            return server_url
    
    # Fall back to the first available server
    return servers[0].get("url", "http://localhost:3000")

spec = load_spec(api_specs_path)

# Initialise async Ollama‑compatible OpenAI client
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="does-not-matter",
)

def clean_snippet(snippet: str) -> str:
    """Remove Markdown fences and duplicate imports from the LLM response."""
    lines = []
    for line in snippet.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):          # skip fences
            continue
        if stripped.startswith("import ") or stripped.startswith("from "):
            continue
        lines.append(line)
    return "\n".join(lines).strip()

def _group_key_from_route(route: str) -> str:
    """First path segment used to group routes."""
    parts = [p for p in route.split("/") if p]
    return parts[0] if parts else "root"

def _sanitized_group_filename(group: str) -> str:
    """Filename pattern: test_<group>.py"""
    safe = group.replace("{", "").replace("}", "").replace("-", "_")
    return f"test_{safe}.py"

async def get_active_model() -> str:
    """Fetch the current active model from the Llama server."""
    try:
        models = await client.models.list()
        if models.data:
            return models.data[0].id
    except Exception as e:
        print(f"Failed to fetch active model: {e}", file=sys.stderr)
    return "gpt-oss:120b-cloud"

async def generate_test_async(endpoint: str, method: str, operation: dict) -> str:
    """Async call to the LLM – returns the raw response string."""
    description = operation.get("description", "")
    request_body = operation.get("requestBody", {})
    responses = operation.get("responses", {})

    prompt = (
        instruction_template
        .replace("{{endpoint}}", endpoint)
        .replace("{{method}}", method.upper())
        .replace("{{description}}", description)
        .replace("{{request_body}}", json.dumps(request_body, indent=2))
        .replace("{{responses}}", json.dumps(responses, indent=2))
        .replace("{{base_url}}", get_base_url(spec))
        .replace("{{framework}}", framework)
        .replace("{{language}}", language)
    )

    model = await get_active_model()
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert QA Engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM error for {method.upper()} {endpoint}: {e}", file=sys.stderr)
        return f"# Failed to generate test for {method.upper()} {endpoint}: {e}"

async def _worker(semaphore: asyncio.Semaphore, route: str, method: str, operation: dict):
    """Wrap generate_test_async with a semaphore to limit concurrency."""
    async with semaphore:
        raw = await generate_test_async(route, method, operation)
    cleaned = clean_snippet(raw)
    group = _group_key_from_route(route)
    return group, cleaned

async def main():
    semaphore = asyncio.Semaphore(max_concurrency)

    # Extract base URL from the spec
    base_url = get_base_url(spec)

    # Build a flat list of tasks (one per endpoint/method)
    tasks = [
        _worker(semaphore, route, method, operation)
        for route, methods in spec.get("paths", {}).items()
        for method, operation in methods.items()
    ]

    # Run all LLM calls concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Aggregate cleaned snippets by group
    tests_by_group: dict[str, list[str]] = {}
    for result in results:
        if isinstance(result, Exception):
            # Already logged inside generate_test_async; just skip
            continue
        group, cleaned_code = result
        tests_by_group.setdefault(group, []).append(cleaned_code)

    # ---------- Write one file per group ----------
    for group, snippets in tests_by_group.items():
        filename = _sanitized_group_filename(group)
        file_path = output_dir / filename

        file_contents = [
            f"# Auto‑generated tests for group: {group}",
            f"# Language: {language}",
            f"# Framework: {framework}",
            "",
        ]

        for snippet in snippets:
            file_contents.append(snippet)
            file_contents.append("")   # blank line between tests

        try:
            file_path.write_text("\n".join(file_contents), encoding="utf-8")
            print(f"✅ Test file written: {file_path}")
        except Exception as e:
            print(f"Failed to write {file_path}: {e}", file=sys.stderr)

# Run the async main entry‑point
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    elapsed = time.time() - start_time
    print(f"⏱️ Execution time: {elapsed:.2f} seconds")
    sys.exit(0)