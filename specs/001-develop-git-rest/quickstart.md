# Quickstart: git-rest Content Management Backend

## Prerequisites
- Python 3.12+
- Docker or Podman (for containerized deployment)
- Git installed on server

## Setup (Development)
1. Clone the repository:
   ```sh
   git clone <your-git-rest-repo-url>
   cd git-rest
   ```
2. Create and activate a Python environment (recommended: uv):
   ```sh
   uv venv .venv
   source .venv/bin/activate
   uv pip install -e .[dev]
   ```

3. Add new dependencies (if needed)
    ```sh
    uv add <package>
    ```

4. Automated Quality Assurance

    ### Unit Testing
    ```sh
    uv run pytest
    ```

    ### Acceptance Testing
    ```sh
    uv run behave
    ```

    ### Linting
    ```sh
    uv run ruff check src
    ```

    ### Formatting
    ```sh
    uv run ruff format src
    ```

5. Set environment variables (example):
   ```sh
   export GIT_REST_SECRET_KEY="your-secret-key"
   export GIT_REST_WORKDIR="/path/to/working/dir"
   ```

6. Run the Flask app (development):
   ```sh
   uv run flask --app src.git_rest.app run --debug
   ```

## Setup (Production)
1. Build and run with Docker:
   ```sh
   docker build -t git-rest .
   docker run -d -p 8000:8000 \
     -e GIT_REST_SECRET_KEY=your-secret-key \
     -e GIT_REST_WORKDIR=/data/repos \
     git-rest
   ```
2. Use Nginx as a reverse proxy for HTTPS, static files, and security.
3. For Kubernetes, create a deployment using the provided Docker image and configure environment variables/secrets.

## API Usage
- See OpenAPI contract in `specs/001-develop-git-rest/contracts/openapi.yaml` for endpoints and request/response formats.



## Notes
- All configuration is via environment variables; never hardcode secrets.
- All user input is validated with pydantic.
- Never expose internal server errors or stack traces in API responses.
- For extensibility, use Flask Blueprints and the application factory pattern.
