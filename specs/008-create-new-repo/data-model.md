# Data Model: Create New Repo

## Entities

### Repository
- **name**: string (unique per user, required)
- **description**: string (required)
- **owner**: User reference (required)
- **files**: list of File (README.md, LICENSE, user-uploaded files)
- **branches**: list of Branch
- **created_at**: datetime
- **updated_at**: datetime
- **license**: string (optional, must match supported list)

### User
- **id**: string (unique, required)
- **username**: string (unique, required)
- **email**: string (unique, required)

### File
- **name**: string
- **content**: string or binary
- **path**: string
- **size**: integer

### Branch
- **name**: string
- **created_at**: datetime

## Validation Rules
- Repository name must be unique per user
- Required fields: name, description, owner
- License must be from supported list or error returned
- README.md content is optional
- File size and repo size limits enforced (see constraints)
