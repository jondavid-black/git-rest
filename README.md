
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

## Development Process
Git-REST development heavily relies on GenAI technology.
This repo uses GitHub Copilot and the GitHub Speckit extensions.
The general workflow for starting new work should use the Speckit workflow in the GitHub Copilot Agent:
- `/speckit.specify <Your high level requirements here>`
- `/speckit.clarity`
- `/speckit.plan`
- `/speckit.tasks`
- `/speckit.analyze`
- `/speckit.checklist`
- `Review the checklists.  Mark all items that have been completed.  Ask any questions you need to mark the others.`

Completing these commands should establish a detailed plan to guide GitHub Copilot through the implementation phases.
Occasionally you may need to nudge the AI as you work through this process by answering questions or providing clarification.
Before proceeding open up any files in the `/specs/<item>/checklists` folder to ensure everything is marked complete.
Once you have completed these AI commands it is recommended to commit and push before beginning implementation.
Note that this process will automatically create and work within a new branch based on the first few words you enter into the high level requirements text.
I like to create a new PR at this time so I can easily monitor CI throughout the implementation process.

To implement the plan use the `/speckit.implement` command in the GitHub Copilot Agent.
This will cause the AI to step through the plan and associated

---
For more, see the API docs and OpenAPI spec.
