# Data Model: Explicit Clone URL API Endpoint

## Entities

### User
- user_id: string (unique)
- Attributes: name, email, etc. (as per existing system)

### Repository
- name: string (unique per user)
- url: string (clone source)
- owner: user_id
- status: enum (e.g., cloned, error)

## Relationships
- User owns multiple repositories
- Repository belongs to one user

## Validation Rules
- Repository name must be unique per user
- Clone URL must be valid and reachable
- Permission checks for user access
- Error states for invalid URL, permission denied, duplicate name
