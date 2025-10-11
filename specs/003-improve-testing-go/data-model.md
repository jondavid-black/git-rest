# Data Model: Improve Testing

## Entities

### Repository
- name: string
- url: string
- branches: list of Branch
- current_state: string

### Branch
- name: string
- commit_history: list of Commit
- current_status: string

### Commit
- id: string
- message: string
- author: string
- timestamp: datetime
- changes: list of FileChange

### FileChange
- file_path: string
- diff: string

### TestCase
- target_function: string
- scenario: string
- expected_outcome: string
- coverage: float
- type: enum [unit, bdd]

## Relationships
- Repository has many Branches
- Branch has many Commits
- Commit has many FileChanges
- TestCase targets a function (by name)

## Validation Rules
- Every Repository must have at least one Branch
- Every Branch must have at least one Commit
- Every TestCase must specify a target_function and expected_outcome
