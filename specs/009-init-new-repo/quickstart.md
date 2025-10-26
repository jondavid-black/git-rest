# Quickstart: Init New Repo API Endpoint

## 1. Create a New Repository

Send a POST request to `/users/<user_id>/repos/init` with JSON body:

```
{
  "repo_name": "my-new-repo"
}
```

- On success, response contains:
  ```
  {
    "url": "https://your-server/users/<user_id>/repos/my-new-repo"
  }
  ```
- On error, response contains an error message and appropriate status code (400, 404, 500).

## 2. Requirements
- Repository name must be unique for the user and match: letters, numbers, dashes, underscores.
- User ID must exist.

## 3. Documentation
- See `api.md`, `getting-started.md`, and `how-to.md` for more details.

## 4. Testing
- Unit and BDD tests are required for this endpoint.
