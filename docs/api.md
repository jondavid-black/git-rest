# API Reference

The full OpenAPI contract is available at [specs/001-develop-git-rest/contracts/openapi.yaml](../specs/001-develop-git-rest/contracts/openapi.yaml).


## Repository Management Endpoints

### `GET /repos`
List all available repositories managed by the backend.

**Response:**
- 200 OK: JSON array of repository objects.

### `POST /repos`
Clone a new repository into the backend-managed workspace.

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

### `GET /repos/{repo_id}`
Get details for a specific repository.

**Response:**
- 200 OK: JSON object of the repository
- 404 Not Found: Error message

### `POST /repos/{repo_id}`
Switch the active repository context for the current user/session.

**Response:**
- 200 OK: Confirmation message and repository object
- 404 Not Found: Error message

See the OpenAPI spec for full request/response details and additional endpoints.
