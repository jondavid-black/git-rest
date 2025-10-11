# Getting Started

This guide will help you get up and running with git-rest.

## Prerequisites
- Python 3.12+
- Docker (optional, for container deployment)
- Git

## Installation
See [../quickstart.md](../specs/001-develop-git-rest/quickstart.md) for full setup instructions.

## Running the API

1. Set environment variables as described in [Environment Setup](environment.md).
2. Start the Flask app:
   ```sh
   uv run flask --app src.git_rest.app run --debug
   ```
3. Access the API at `http://localhost:5000/` (default).

For production, see Docker and Nginx setup in the documentation.
