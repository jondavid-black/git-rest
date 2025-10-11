
# API Reference


The full OpenAPI contract is available at [specs/001-develop-git-rest/contracts/openapi.yaml](../specs/001-develop-git-rest/contracts/openapi.yaml).

## Authentication & Environment

- All endpoints require a JWT access token in the `Authorization` header: `Bearer <token>`
- Obtain a token via the `/login` endpoint (see README for usage)
- Set the environment variable `GIT_REST_SECRET_KEY` to a strong, random value in production
- Optionally set `GIT_REST_WORKDIR` to control the repository storage location




## User-Scoped Repository Management Endpoints

All endpoints are now scoped by user. Replace `{user_id}` with the authenticated user's ID.

### `GET /users/{user_id}/repos`
List all repositories for the user.

**Response:**
- 200 OK: JSON array of repository objects.

### `POST /users/{user_id}/repos`
Clone a new repository for the user.

**Request JSON:**
```
{
  "name": "repo-name",
  "url": "https://github.com/example/repo.git"
}
```
**Response:**
- 201 Created: JSON object of the new repository
- 400 Bad Request: Error message

### `GET /users/{user_id}/repos/{repo_id}`
Get details for a specific repository.

**Response:**
- 200 OK: JSON object of the repository
- 404 Not Found: Error message

### `POST /users/{user_id}/repos/{repo_id}`
Switch the active repository context for the user.

**Response:**
- 200 OK: Confirmation message and repository object
- 404 Not Found: Error message



## User-Scoped Branch Management Endpoints

### `GET /users/{user_id}/repos/{repo_id}/branches`
List all branches in the specified repository for the user.

**Response:**
- 200 OK: JSON array of branch objects
- 404 Not Found: Error message

### `POST /users/{user_id}/repos/{repo_id}/branches`
Create a new branch in the specified repository for the user.

**Request JSON:**
```
{
  "name": "feature-x"
}
```
**Response:**
- 201 Created: JSON array of branch objects (including the new branch)
- 400 Bad Request: Error message

### `POST /users/{user_id}/repos/{repo_id}/branches/{branch}`
Switch to the specified branch in the repository for the user.

**Response:**
- 200 OK: Confirmation message and repository object
- 400 Bad Request: Error message

### `DELETE /users/{user_id}/repos/{repo_id}/branches/{branch}`
Delete the specified branch from the repository for the user.

**Response:**
- 200 OK: JSON array of remaining branch objects
- 400 Bad Request: Error message


## Commit and Diff Endpoints

### `POST /repos/{repo_id}/commit`
Commit all staged and unstaged changes in the specified repository.

**Request JSON:**
```
{
	"message": "Commit message",
	"author": "Author Name"
}
```
**Response:**
- 201 Created: JSON object of the new commit
- 400 Bad Request: Error message

### `GET /repos/{repo_id}/diff`
Get the diff for the working tree or between two commits in the specified repository.

**Query Parameters:**
- `a`: (optional) Commit hash A
- `b`: (optional) Commit hash B

**Response:**
- 200 OK: JSON object with `diff` string
- 400 Bad Request: Error message




## User-Scoped File Delivery Endpoints

### `GET /users/{user_id}/repos/{repo_id}/files`
List files and directories in the user's repository. Optionally provide a `path` query parameter to list a subdirectory.

**Query Parameters:**
- `path`: (optional) Relative path within the repository to list (default: root).

**Response:**
- 200 OK: JSON array of file/directory entries:
  - `path`: Relative path
  - `type`: "file", "dir", or "symlink"
  - `size`: File size in bytes
  - `last_modified`: ISO8601 timestamp
- 400 Bad Request: Error message

### `GET /users/{user_id}/repos/{repo_id}/files/{file_path}`
Get the contents of a file for the user. If the file is small, returns the content directly. If the file is large, returns a redirect to a secure download URL.

**Response:**
- 200 OK: File content (inline)
- 302 Found: JSON with `{ "redirect": true, "url": "..." }` for large files
- 404 Not Found: Error message
- 400 Bad Request: Error message

### `GET /users/{user_id}/repos/{repo_id}/files/{file_path}/download`
Download a file securely using a signed URL. Requires `expires` and `token` query parameters (provided by the redirect from the previous endpoint).

**Query Parameters:**
- `expires`: Expiry timestamp (required)
- `token`: Secure token (required)

**Response:**
- 200 OK: File download (attachment)
- 403 Forbidden: Invalid or expired token
- 404 Not Found: Error message
- 400 Bad Request: Error message


## Concurrency Guarantees & Usage

### Concurrent User Operations

- All repository, branch, and file operations are concurrency-safe for multiple users.
- Each user's data is isolated in a separate directory/namespace; no cross-user access is possible.
- File-based locking ensures that concurrent actions (e.g., two users creating branches or files at the same time) are serialized per user, preventing race conditions and data corruption.
- The system supports at least 10 concurrent users with no more than 10% increase in average operation latency (see non-functional requirements).

### Audit Logging Under Concurrency

- All user actions are logged to a per-user audit log file.
- Audit log entries are written atomically, so concurrent actions are always recorded and never lost or interleaved.
- Each log entry includes user ID, action type, resource, timestamp, and outcome.

### Best Practices

- For best performance, avoid long-running operations in a single request.
- If you need to coordinate actions across multiple users, do so at the application level (not via the API).

### Example: Simultaneous Repository Operations

Two users can create, modify, and delete repositories, branches, and files at the same time. Each user's changes are isolated and do not affect other users.

See the OpenAPI spec for full request/response details and additional endpoints.
