# Data Model: Multi-Repo Testing

## Entities

### User
- id: string
- username: string
- [other attributes as per existing system]

### Repository
- name: string (unique per user)
- path: string (filesystem location)
- origin_url: string (remote URL)
- owner_id: string (user id)
- state: enum [cloned, active, error, ...]
- [other git metadata as needed]

### Session/Context
- user_id: string
- active_repo: string (repo name or id)

## Relationships
- User 1---* Repository (a user can have multiple repos)
- User 1---1 Session/Context (one active context per user)

## Validation Rules
- Repository names must be unique per user
- Origin URL must be a valid git remote
- Only one active repo per user session
- Commits/changes in one repo must not affect others
- Errors (e.g., name collision) must be reported clearly
