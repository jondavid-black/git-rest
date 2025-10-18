# Quickstart: Exception Exposure - Secure Error Responses

## Prerequisites
- Python 3.12+
- Flask, GitPython, Pydantic installed
- pytest, Behave for testing

## Setup
1. Clone the repository and checkout branch `007-exception-exposure-there`
2. Install dependencies:
   ```sh
   uv pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```sh
   uv run python main.py
   ```
4. Trigger an error via API to verify secure error response

## Testing
- Run unit tests:
  ```sh
  uv run pytest
  ```
- Run acceptance tests:
  ```sh
  uv run behave
  ```

## Key Endpoints
- All error responses are sanitized and user-friendly
- Internal error logs available for developer diagnostics

## Notes
- Error logs may include user data and are accessible to all developers
- No raw exception content or stack traces exposed to users
