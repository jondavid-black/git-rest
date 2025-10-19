

# Feature Specification: Create & Clone Repo


**Feature Branch**: `008-create-new-repo`  
**Created**: 2025-10-19  
**Status**: Draft  
**Input**: Add API endpoints for users to (a) create a new repository from scratch, and (b) clone an existing remote repository. Both endpoints must be simple, robust, and independently testable.


## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a New Repository (P1)
A user creates a new repository by providing a name and description. Optionally, they may include README content and a license name. The system creates the repository and returns confirmation.

**Acceptance Criteria:**
1. Given a valid repo name and description, when the user submits a create request, then a new repository is created and confirmation is returned.
2. Given README content, when included, then the repository contains a README.md file with the provided content.
3. Given a supported license name, when included, then the repository contains a LICENSE file with the correct license text.
4. Duplicate repo names for the same user are rejected with a clear error.
5. Missing required fields (name, description) are rejected with a clear error.
6. Unsupported license names are rejected with a clear error.

### User Story 2 - Clone a Remote Repository (P1)
A user clones a remote repository by providing a remote URL (and optionally a new name/description). The system clones the repo and returns confirmation.

**Acceptance Criteria:**
1. Given a valid remote URL, when the user submits a clone request, then the repository is cloned and confirmation is returned.
2. If a new name is provided, the cloned repo uses that name; otherwise, it uses the default name from the remote.
3. Duplicate repo names for the same user are rejected with a clear error.
4. Invalid or unreachable remotes are rejected with a clear error.
5. Missing required fields (remote URL) are rejected with a clear error.

### User Story 3 - Perform Git Operations on New/Cloned Repo (P2)
After creation or cloning, a user can post files, create branches, and perform other git operations using the API.

**Acceptance Criteria:**
1. Given a new or cloned repository, when the user posts a file, then the file is added to the repository.
2. Given a new or cloned repository, when the user creates a branch, then the branch is created and available for use.

### Edge Cases
- Duplicate repo names for the same user
- Unsupported or misspelled license names
- Invalid or unreachable remote URLs
- Empty or very large README content
- Missing required fields (name, description, remote URL)


## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an API endpoint for creating a new repository (`POST /api/repos/create`).
- **FR-002**: System MUST provide an API endpoint for cloning a remote repository (`POST /api/repos/clone`).
- **FR-003**: System MUST require a repository name and description for creation; and a remote URL for cloning.
- **FR-004**: System MUST allow optional README.md content and license name for creation.
- **FR-005**: System MUST return a confirmation and repository details upon successful creation or clone.
- **FR-006**: System MUST prevent creation or cloning of repositories with duplicate names for the same user/namespace.
- **FR-007**: System MUST allow all standard git-rest operations (file upload, branch creation, etc.) on new or cloned repositories.
- **FR-008**: System MUST validate required fields and return errors for missing or invalid input.
- **FR-009**: System MUST handle unsupported or misspelled license names and invalid remote URLs gracefully, providing a clear error.


### Key Entities
- **Repository**: User-owned project, with: name, description, files, branches, license, owner.
- **User**: The actor creating and managing repositories.


## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Users can create or clone a repository with required and optional fields in under 30 seconds.
- **SC-002**: 100% of valid create/clone requests result in a usable repository with correct files and metadata.
- **SC-003**: 95% of users are able to perform follow-up git operations (file upload, branch creation) on new or cloned repos without errors.
- **SC-004**: System returns clear, actionable error messages for all invalid or unsupported input cases.


## Assumptions
- If a license name is not recognized, the system will return an error rather than guessing.
- README.md content is optional and may be empty.
- Repository names are case-sensitive unless otherwise specified.
- Users are authenticated and authorized to create or clone repositories.
