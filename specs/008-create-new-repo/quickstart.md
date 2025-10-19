# Quickstart: Create New Repo

## 1. Create a Repository
- Send a POST request to `/api/repos` with JSON body:
  ```json
  {
    "name": "my-repo",
    "description": "A new project",
    "readme": "# My Repo\nWelcome!",
    "license": "MIT"
  }
  ```
- On success, response includes repo details and confirmation.

## 2. Add Files
- Use the file upload API to add files to the new repository.

## 3. Create Branches
- Use the branch API to create new branches as needed.

## 4. Perform Other Git Operations
- All standard git-rest API operations are available on the new repository.

## 5. Error Handling
- If a repo name already exists for the user, an error is returned.
- If the license is not recognized, an error is returned.
- Missing required fields result in a validation error.
