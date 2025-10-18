# Data Model for Update the API to allow a user to POST file content

## Entities

### File
- **Attributes**:
  - path: string
  - type: enum (text, binary)
  - content: string (text or base64-encoded binary)
  - status: enum (staged, unstaged)
  - last_updated: datetime
  - locked: boolean

### Repository
- **Attributes**:
  - name: string
  - branch: string
  - files: list[File]
  - last_commit: string

### User
- **Attributes**:
  - user_id: string
  - permissions: list[string]

## Validation Rules
- File path must be valid and exist in repo (or be creatable).
- File type must be recognized (text or binary).
- Content must match encoding for type.
- Only one update allowed per file at a time (sequential locking).
- Branch must exist and be current.

## State Transitions
- File status: unstaged → staged (on POST)
- File locked: false → true (during update), true → false (after update)
- Repository: branch may change (if user switches context)
