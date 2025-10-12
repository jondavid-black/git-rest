
# Feature Specification: Multi-Repo Testing

**Feature Branch**: `004-multi-repo-testing`  
**Created**: 2025-10-12  
**Status**: Draft  
**Input**: User description: "Multi-Repo Testing - Add new BDD tests to ensure git-rest works as expected for a single user with multiple repositories being managed within the API.  Use the following test repos:  https://github.com/jondavid-black/git-rest-test and https://github.com/jondavid-black/git-rest-test-other.  Ensure both repos can be cloned by the user.  Ensure the user can switch between repos.  Ensure commits made to one repo do not have any effect on the other repo.  Ensure the origin of each repo is correctly maintained."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clone Multiple Repositories (Priority: P1)

A user can clone both provided repositories into the system using the API, and each is managed independently.

**Why this priority**: Cloning is the foundational action for multi-repo management; without it, no further actions are possible.

**Independent Test**: Can be fully tested by attempting to clone both repositories and verifying their presence and independence in the system.

**Acceptance Scenarios**:

1. **Given** a user with access to the API, **When** they request to clone `git-rest-test`, **Then** the repository is cloned and available for operations.
2. **Given** a user with access to the API, **When** they request to clone `git-rest-test-other`, **Then** the repository is cloned and available for operations.
3. **Given** both repositories are cloned, **When** the user lists their repositories, **Then** both are shown as separate entities.

---

### User Story 2 - Switch Between Managed Repositories (Priority: P2)

A user can switch their active context between the two managed repositories via the API.

**Why this priority**: Switching context is essential for workflows involving multiple repositories, ensuring the user can operate on the intended repo.

**Independent Test**: Can be tested by switching context and verifying subsequent actions apply to the selected repository only.

**Acceptance Scenarios**:

1. **Given** both repositories are cloned, **When** the user switches context to `git-rest-test`, **Then** all subsequent actions apply only to that repository.
2. **Given** both repositories are cloned, **When** the user switches context to `git-rest-test-other`, **Then** all subsequent actions apply only to that repository.

---

### User Story 3 - Isolated Commits and Repository State (Priority: P3)

Commits made to one repository do not affect the state or history of the other repository.

**Why this priority**: Ensures data integrity and isolation between repositories, which is critical for correct multi-repo management.

**Independent Test**: Can be tested by making a commit in one repository and verifying no changes in the other.

**Acceptance Scenarios**:

1. **Given** both repositories are cloned, **When** a commit is made to `git-rest-test`, **Then** no changes are reflected in `git-rest-test-other`.
2. **Given** both repositories are cloned, **When** a commit is made to `git-rest-test-other`, **Then** no changes are reflected in `git-rest-test`.

---

### User Story 4 - Repository Origin Integrity (Priority: P4)

The origin (remote URL) of each repository is correctly maintained and can be verified via the API.

**Why this priority**: Ensures that repository remotes are not mixed up, which is essential for correct push/pull operations.

**Independent Test**: Can be tested by querying the origin of each repository and confirming it matches the expected remote URL.

**Acceptance Scenarios**:

1. **Given** both repositories are cloned, **When** the user queries the origin of `git-rest-test`, **Then** the correct remote URL is returned.
2. **Given** both repositories are cloned, **When** the user queries the origin of `git-rest-test-other`, **Then** the correct remote URL is returned.

---

### Edge Cases

- What happens if the user attempts to clone a repository with the same name as an existing one?
- How does the system handle switching to a repository that does not exist or is not managed?
- What if a commit is attempted in a repository that is in a detached HEAD state?
	- **Acceptance Criterion**: The system MUST return a clear error message and prevent the commit. A BDD test must verify that attempting a commit in detached HEAD results in an actionable error and no changes to repo state.
- How does the system handle network failures during clone or commit operations?

## Requirements *(mandatory)*
### Definitions

- **Independent state**: Each repository's data, history, and configuration are stored and managed separately, with no shared state or side effects between repositories.
- **Isolation**: Actions (such as commits, switches, or queries) performed on one repository have no effect on any other managed repository.
- **Origin integrity**: The remote URL (origin) for each repository must always match the value provided at clone time, unless explicitly changed by the user.
- **Correct remote**: The origin URL returned by the API for a repository must match the expected remote URL for that repository.
- **Clear error message**: An error message that explicitly states the cause of the failure and, where possible, suggests a corrective action (e.g., "Cannot commit: repository is in detached HEAD state. Please checkout a branch before committing.")

### Functional Requirements

- **FR-001**: System MUST allow a user to clone multiple repositories via the API.
- **FR-002**: System MUST maintain independent state for each managed repository.
- **FR-003**: System MUST allow the user to switch active context between managed repositories.
- **FR-004**: System MUST ensure that commits and changes in one repository do not affect any other managed repository.
- **FR-005**: System MUST provide a way to query the origin (remote URL) of each managed repository.
- **FR-006**: System MUST handle errors gracefully when cloning, switching, or committing fails.
- **FR-007**: System MUST prevent repository name collisions or provide a clear resolution mechanism.  

### Key Entities

- **User**: The actor performing actions via the API.
- **Repository**: Represents a managed git repository, with attributes such as name, path, and origin URL.
- **Session/Context**: Represents the user's current active repository for API operations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully clone and manage at least two repositories in a single session without errors.
- **SC-002**: Switching between repositories is completed in under 2 seconds in 95% of cases.
- **SC-006**: System performance for switching repositories is measured in BDD tests, and 95% of switches complete in under 2 seconds.
- **SC-003**: Commits made to one repository do not appear in the history or state of any other managed repository (100% isolation).
- **SC-004**: The origin URL for each repository is always accurate and matches the expected remote after all operations.
- **SC-005**: 100% of error scenarios (e.g., name collision, network failure) result in clear, actionable error messages to the user.

## Assumptions

- The user is authenticated and authorized to use the API.
- The provided test repositories are publicly accessible and can be cloned without authentication.
- The system supports at least two repositories per user.
- Standard git operations (clone, commit, query remote) are supported by the underlying system.
