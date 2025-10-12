
# How-To Guides

## Cloning a Repository
1. Authenticate and obtain a JWT token.
2. Send a POST to `/users/{user_id}/repos` with JSON:
	```json
	{ "name": "my-repo", "url": "https://github.com/example/repo.git" }
	```
3. On success, you'll receive a 201 response with the new repo details.
4. If the name already exists, you'll get a 400 error.

## Switching Repositories
1. POST to `/users/{user_id}/repos/{repo_id}` to switch the active context.
2. On success, you'll get a confirmation message.
3. If the repo does not exist, you'll get a 404 error.

## Querying Repository Origin
1. GET `/users/{user_id}/repos/{repo_id}/origin` to retrieve the remote/origin URL for a repo.
2. Use this to verify the source of any managed repository.

## Handling Errors
- **Name collision**: 400 error if you try to clone a repo with an existing name.
- **Switching to non-existent repo**: 404 error.
- **Detached HEAD**: 400 error if you try to commit in a detached HEAD state.
- **Network failure**: 400 error if the remote cannot be reached during clone.

## Other Operations
- [Managing Branches](#): List, create, and switch branches via `/branches` endpoints.
- [Committing Changes](#): Commit files with `/commit` endpoints.
- [Viewing Diffs](#): Use `/diff` endpoints to see changes.
- [Retrieving Files](#): Download files via `/files` endpoints.

See the [API Reference](api.md) for full details on all endpoints and request/response formats.
