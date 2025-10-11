
# git-rest

git-rest is a RESTful API to manage server-side content within a git SCM repository.

## Features
- Clone, list, and switch repositories
- Branch management (list, create, switch, delete)
- Commit and diff operations
- Secure file listing, content, and download endpoints
- JWT-based authentication

## Requirements
- Python 3.12+
- Git
- [uv](https://github.com/astral-sh/uv) (for dependency management)

## Setup
1. Clone the repository:
	```bash
	git clone <your-fork-or-upstream-url>
	cd git-rest
	```
2. Install dependencies:
	```bash
	uv pip install -r requirements.txt
	```
3. Set environment variables (required for security):
	- `GIT_REST_SECRET_KEY`: A strong, random secret key for JWT and secure URLs.
	- `GIT_REST_WORKDIR`: (optional) Path for managed repositories (default: `/tmp/git-rest`).

## Running the API
```bash
uvicorn main:app --reload
```
Or use Flask/Gunicorn as configured in your deployment.

## Authentication
All endpoints require a JWT access token. Obtain a token via the `/login` endpoint:

```http
POST /login
{
  "username": "admin",
  "password": "password123"
}
```
Response:
```json
{
  "access_token": "..."
}
```
Include the token in the `Authorization` header for all requests:
```
Authorization: Bearer <access_token>
```

## API Reference
See `docs/api.md` for endpoint documentation and `specs/001-develop-git-rest/contracts/openapi.yaml` for the OpenAPI contract.

## Quickstart Example
```bash
# List repositories
curl -H "Authorization: Bearer <token>" http://localhost:8000/repos
# Clone a repo
curl -X POST -H "Authorization: Bearer <token>" -d '{"name": "myrepo", "url": "https://github.com/example/repo.git"}' http://localhost:8000/repos
```

## Security Notes
- Always set a strong `GIT_REST_SECRET_KEY` in production.
- The demo user/password is for development only. Integrate with a real user management system for production.

---
For more, see the API docs and OpenAPI spec.
