# Quickstart: Explicit Clone URL API Endpoint

## How to Clone a Repository

1. Send a POST request to `/api/<user_id>/repos/clone` with the clone URL in the request body.
2. On success, the repository will be available in the user's namespace.
3. On error (invalid URL, permission, duplicate), review the error message and correct the request.

## Example Request

```
POST /api/123/repos/clone
Content-Type: application/json

{
  "url": "https://github.com/example/repo.git"
}
```

## Notes
- The old endpoint `/api/<user_id>/repos/` no longer supports cloning.
- All documentation and tests reference the new endpoint.
