
# Getting Started

Welcome to **git-rest**! This guide will help you get up and running with the multi-repo REST API for Git.

## Key Features
- **Multi-repo support**: Manage multiple repositories per user, each fully isolated.
- **User isolation**: All operations are scoped to the authenticated user.
- **Origin integrity**: Query and verify the remote/origin for any managed repo.
- **Repository status**: Instantly check branch, cleanliness, and file status for any repo.
- **Fast context switching**: Switch between repos in under 2 seconds (95% of cases).
- **Robust error handling**: Clear errors for name collisions, non-existent repos, detached HEAD, and network failures.

## Prerequisites
- Python 3.12+
- Docker (optional, for container deployment)
- Git

## Quickstart
See [Quickstart](specs/001-develop-git-rest/quickstart.md) for full setup instructions.

## Running the API

### 1. Set Environment Variables
See [Environment Setup](environment.md) for details. At minimum, set:

```sh
export GIT_REST_SECRET_KEY="your-secret-key"
export GIT_REST_WORKDIR="/absolute/path/to/repos"
# Optional: Enable interactive API docs UI
export GIT_REST_UI=1
# Optional: Enable debug logging
export GIT_REST_DEBUG=1
```

Or copy and edit `.env.example`:

```sh
cp .env.example .env
# Edit .env with your values
```

### 2. Run the API (Development)

```sh
uv run flask --app src.git_rest.app run --debug
```
Access at [http://localhost:5000/](http://localhost:5000/)

### 3. Run with Gunicorn (Production)

```sh
uv run gunicorn -b 0.0.0.0:8000 "src.git_rest.app:create_app()"
```

Alternatively you can set the environment variables and run the server in a single CLI command.

```sh
GIT_REST_WORKDIR="/absolute/path/to/repos" GIT_REST_UI=1 uv run gunicorn -b 0.0.0.0:8000 "src.git_rest.app:create_app()"
```

Access at:
- BaseURL: [http://localhost:8000/](http://localhost:8000/)
- Health: [http://localhost:8000/healthz](http://localhost:8000/healthz)
- API Docs: [http://localhost:8000/apidocs](http://localhost:8000/apidocs)

#### Docker Example
To run in Docker (see `Dockerfile`):

```sh
docker build -t git-rest .
docker run -e GIT_REST_SECRET_KEY=your-secret-key -e GIT_REST_WORKDIR=/data/repos -p 8000:8000 git-rest
```

---

For advanced production, see Docker and Nginx setup in the documentation.

## Next Steps
- See the [How-To Guides](how-to.md) for common workflows.
- Explore the [API Reference](api.md) for endpoint details.
