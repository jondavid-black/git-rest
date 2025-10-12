
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
1. Set environment variables as described in [Environment Setup](environment.md).
2. Start the API server:
   ```sh
   uv run flask --app src.git_rest.app run --debug
   ```
3. Access the API at `http://localhost:5000/` (default).

For production, see Docker and Nginx setup in the documentation.

## Next Steps
- See the [How-To Guides](how-to.md) for common workflows.
- Explore the [API Reference](api.md) for endpoint details.
