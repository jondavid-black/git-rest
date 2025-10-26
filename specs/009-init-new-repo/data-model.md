# Data Model for Init New Repo API Endpoint

## Entities

### User
- user_id: string (unique, required)
- name: string (required)

### Repository
- repo_name: string (unique per user, required, git naming rules)
- owner: string (user_id, required)
- url: string (required)
- creation_date: datetime (required)

## Relationships
- User 1:N Repository (a user can own multiple repositories)

## Validation Rules
- repo_name must match: ^[A-Za-z0-9_-]+$
- repo_name must be unique for the user
- user_id must exist

## State Transitions
- Repository: [uninitialized] → [initialized] (on creation)
