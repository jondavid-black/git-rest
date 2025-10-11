# Quickstart: Segregate Backend by User ID

## Overview
This feature ensures that all backend operations are segregated by user ID, so that multiple users can manage repositories, branches, and files without impacting each other. All file system operations are scoped to a user's namespace/directory.

## Prerequisites
- Python 3.12+
- Flask, gitpython, pydantic
- pytest, Behave, uv, ruff
- GitHub Actions for CI/CD
- Mkdocs for documentation

## Setup
1. Clone the repository and check out the feature branch:
   ```sh
   git clone <repo-url>
   cd git-rest
   git checkout 002-i-want-to
   ```
2. Install dependencies:
   ```sh
   uv pip install -r requirements.txt
   ```
3. Run tests:
   ```sh
   pytest
   behave
   ```
4. Start the backend server:
   ```sh
   python -m git_rest
   ```

## API Usage
- All endpoints are scoped under `/users/{user_id}/...`.
- Users can create, modify, and delete repositories, branches, and files in their own namespace.
- No cross-user access is permitted.

## Example: Create a Repository
```sh
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "my-repo"}' \
  http://localhost:5000/api/v1/users/alice/repos
```

## Audit Log
- All user actions are logged and can be retrieved via `/users/{user_id}/audit-log`.

## Notes
- Duplicate repository, branch, and file names are allowed across users, but must be unique within a user's namespace.
- Unauthorized access attempts return HTTP 403 and are logged.
- Audit logs are retained for 1 year.
