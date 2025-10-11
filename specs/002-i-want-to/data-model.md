# Data Model: Segregate Backend by User ID

## Entities

### User
- **user_id**: string (unique, required)
- **Attributes**: Authenticated identity; not responsible for authentication mechanism (assumed provided)

### Repository
- **repo_id**: string (unique within user namespace)
- **name**: string
- **owner_user_id**: string (references User)
- **Attributes**: All repository data is stored in a directory under the user's namespace

### Branch
- **branch_id**: string (unique within repository)
- **name**: string
- **repository_id**: string (references Repository)

### File
- **file_id**: string (unique within branch/repository)
- **path**: string
- **repository_id**: string (references Repository)
- **branch_id**: string (references Branch)
- **owner_user_id**: string (references User)

### Audit Log
- **log_id**: string (unique)
- **user_id**: string (references User)
- **action_type**: string (e.g., create, delete, update, read)
- **target_resource**: string (repo/branch/file identifier)
- **timestamp**: datetime
- **outcome**: string (success/failure, error code)
- **retention**: 1 year

## Relationships
- User 1:N Repository
- Repository 1:N Branch
- Branch 1:N File
- User 1:N Audit Log

## Validation Rules
- All operations must be scoped to the current user's namespace/directory
- No cross-user access permitted
- Repository, branch, and file names must be unique within the user's namespace, but may duplicate across users
- Audit log must record all user actions and be retained for 1 year

## State Transitions
- Repository/branch/file lifecycle: create → update → delete (all scoped to user)
- Audit log: append-only, no modification after write

---

All entities and rules derived from the feature spec and clarifications.
