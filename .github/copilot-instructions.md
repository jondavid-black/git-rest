# git-rest Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-10-11

## Active Technologies
- Python 3.12+ + Flask (with Blueprints, application factory pattern), gitpython, pydantic, Gunicorn, Nginx (reverse proxy), Docker, pytest, Behave, uv, ruff (001-develop-git-rest)
- Python 3.12+ + Flask, gitpython, pydantic (002-i-want-to)
- Filesystem (user data in separate directories/namespaces) (002-i-want-to)
- Python 3.12+ + Flask, gitpython, pydantic, pytest, Behave, uv, ruff (003-improve-testing-go)

## Project Structure
```
src/
tests/
```

## Commands
cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style
Python 3.12+: Follow standard conventions

## Recent Changes
- 003-improve-testing-go: Added Python 3.12+ + Flask, gitpython, pydantic, pytest, Behave, uv, ruff
- 002-i-want-to: Adding user data isolation via directory namespacing, audit logging, and concurrent user support
- 001-develop-git-rest: Added Python 3.12+ + Flask (with Blueprints, application factory pattern), gitpython, pydantic, Gunicorn, Nginx (reverse proxy), Docker, pytest, Behave, uv, ruff

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
