# Quickstart: Update the API to allow a user to POST file content

## Prerequisites
- Python 3.12+
- Flask, gitpython, pydantic installed
- Repository initialized and accessible

## API Usage


### 1. POST file content
```
POST /users/{user_id}/repos/{repo_id}/files/{file_path}
Content-Type: application/json
{
  "content": "...",           // text or base64-encoded binary
  "type": "text"|"binary",   // file type
  "partial": {                 // optional for partial update
    "start_line": 10,
    "end_line": 20
  }
}
```
- Stages the file change, does not commit.
- Returns status code 200 on success, error code otherwise.

### 2. GET file content
```
GET /users/{user_id}/repos/{repo_id}/files/{file_path}
```
- Returns file content and metadata.

### 3. Commit staged changes
```
POST /users/{user_id}/repos/{repo_id}/commit
```
- Commits all staged changes.

## Example Workflow
1. Clone repo (e.g., git-rest-test)
2. GET README.md
3. POST new content to README.md (add a line)
4. GET README.md to verify update
5. POST commit to save changes

## Error Handling
- Invalid file path/branch: 404
- Invalid content/type: 400
- Concurrent update: 409 (blocked, retry)

## Notes
- Binary files must be base64-encoded in payload.
- Partial updates supported via line range.
- No commit occurs on file POST; explicit commit required.
