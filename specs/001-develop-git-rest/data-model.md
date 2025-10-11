# Data Model: git-rest Content Management Backend

## Entities

### Repository
- **id**: string (unique, derived from repo path or name)
- **name**: string
- **path**: string (absolute path on server)
- **remotes**: list of Remote
- **branches**: list of Branch
- **current_branch**: string
- **status**: RepoStatus

### Remote
- **name**: string
- **url**: string

### Branch
- **name**: string
- **is_current**: bool

### Commit
- **hash**: string
- **author**: string
- **date**: datetime
- **message**: string
- **parent_hashes**: list of string

### FileEntry
- **path**: string (relative to repo root)
- **type**: enum [file, dir, symlink]
- **size**: int (bytes)
- **last_modified**: datetime

### RepoStatus
- **staged**: list of FileEntry
- **unstaged**: list of FileEntry
- **untracked**: list of FileEntry

## Validation Rules
- All user input (repo names, branch names, file paths) must be validated using pydantic schemas.
- No path traversal (../) or absolute paths allowed in user-supplied file paths.
- Repository names must be unique per backend instance.
- Branch names must conform to git naming rules.

## State Transitions
- Repository: created (cloned) → available → deleted
- Branch: created → checked out → deleted
- FileEntry: added/modified/staged/committed/removed

## Relationships
- Repository has many Branches, Remotes, Commits, and FileEntries
- Branches belong to a Repository
- Commits belong to a Repository (and Branch)
- FileEntries belong to a Repository (and Commit)
