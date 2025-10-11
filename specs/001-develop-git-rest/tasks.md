# Tasks: git-rest Content Management Backend

## Feature: git-rest Content Management Backend

---

## Phase 1: Setup Tasks

- T001: [P] Initialize Python 3.12+ project with Flask, gitpython, pydantic, Gunicorn, Nginx, Docker, pytest, Behave, uv, ruff (src/, tests/, docs/)
- T002: [P] Set up project structure: src/git_rest/, tests/unit/, tests/bdd/, docs/, specs/001-develop-git-rest/
- T003: [P] Configure environment variables and secrets management (GIT_REST_SECRET_KEY, GIT_REST_WORKDIR)
- T004: [P] Set up Mkdocs + Material for documentation
- T005: [P] Set up GitHub Actions for CI (pytest, Behave, ruff, build, tag, release)
- T006: [P] Add Dockerfile and containerization scripts
- T007: [P] Add .env.example and document environment setup

## Phase 2: Foundational Tasks (Blocking Prerequisites)

- T008: Implement pydantic validation schemas for all user input (repo, branch, file names)
- T009: Implement authentication/authorization middleware (OAuth2/JWT)
- T010: Implement error handling and logging infrastructure
- T011: Implement base Flask app factory and blueprint registration
- T012: Implement file system isolation and path validation logic

---

## Phase 3: User Story 1 - Clone and Switch Repositories (P1)

**Goal**: User can clone a remote repository, list available repositories, and switch between them via API.

**Independent Test Criteria**: Can clone, list, and switch repositories via API calls; all subsequent operations apply to selected repo.

- T013: [P] Implement Repository model and storage logic (src/git_rest/models/repository.py)
- T014: [P] Implement /repos (GET: list, POST: clone) endpoints (src/git_rest/api/repos.py)
- T015: [P] Implement /repos/{repo_id} (GET: details, POST: switch) endpoint
- T016: [P] Implement repository switching logic in backend context
- T017: [P] Add BDD acceptance tests for clone/list/switch (tests/bdd/features/repos.feature)
- T018: [P] Add unit tests for repository operations (tests/unit/test_repository.py)
- T019: [P] Document repository management API (docs/api.md)
- T020: [P] Add audit logging for repository operations

**Checkpoint: US1 complete**

---

## Phase 4: User Story 2 - Manage Branches (P2)

**Goal**: User can list, create, remove, and switch branches in a selected repository via API.

**Independent Test Criteria**: Can create, list, switch, and delete branches via API; repo state updates accordingly.

- T021: [P] Implement Branch model (src/git_rest/models/branch.py)
- T022: [P] Implement /repos/{repo_id}/branches (GET: list, POST: create) endpoints
- T023: [P] Implement /repos/{repo_id}/branches/{branch} (POST: switch, DELETE: remove) endpoints
- T024: [P] Add BDD acceptance tests for branch management (tests/bdd/features/branches.feature)
- T025: [P] Add unit tests for branch operations (tests/unit/test_branch.py)
- T026: [P] Document branch management API (docs/api.md)
- T027: [P] Add audit logging for branch operations

**Checkpoint: US2 (branches) complete**

---

## Phase 5: User Story 2 - Commit and Diff Changes (P2)

**Goal**: User can commit changes to files and view diffs between commits using the API.

**Independent Test Criteria**: Can commit file changes and retrieve diffs via API; commits visible in log.

- T028: [P] Implement Commit model (src/git_rest/models/commit.py)
- T029: [P] Implement /repos/{repo_id}/commit (POST: commit) endpoint
- T030: [P] Implement /repos/{repo_id}/diff (GET: diff) endpoint
- T031: [P] Add BDD acceptance tests for commit/diff (tests/bdd/features/commit_diff.feature)
- T032: [P] Add unit tests for commit/diff logic (tests/unit/test_commit.py)
- T033: [P] Document commit/diff API (docs/api.md)
- T034: [P] Add audit logging for commit/diff operations

**Checkpoint: US2 (commit/diff) complete**

---

## Phase 6: User Story 3 - Content Delivery (P3)

**Goal**: User can retrieve file contents or listings, with small files returned directly and large files redirected to a secure URL.

**Independent Test Criteria**: Can request files of various sizes and receive correct delivery method (inline or redirect).

- T035: [P] Implement FileEntry model (src/git_rest/models/file_entry.py)
- T036: [P] Implement /repos/{repo_id}/files (GET: list) endpoint
- T037: [P] Implement /repos/{repo_id}/files/{file_path} (GET: content/redirect) endpoint
- T038: [P] Implement secure URL generation for large files (src/git_rest/services/secure_url.py)
- T039: [P] Add BDD acceptance tests for file delivery (tests/bdd/features/file_delivery.feature)
- T040: [P] Add unit tests for file delivery logic (tests/unit/test_file_entry.py)
- T041: [P] Document file delivery API (docs/api.md)
- T042: [P] Add audit logging for file delivery operations

**Checkpoint: US3 complete**

---

## Final Phase: Polish & Cross-Cutting Concerns

- T043: [P] Add API versioning and OpenAPI documentation (docs/api.md, openapi.yaml)
- T044: [P] Add configuration for file size threshold (inline vs. redirect)
- T045: [P] Add production deployment scripts and documentation (Docker, Nginx, Gunicorn)
- T046: [P] Add security review and penetration test checklist
- T047: [P] Add performance/load test scripts
- T048: [P] Finalize and publish Mkdocs documentation

---

## Dependencies

- Phase 1 and 2 must complete before any user story phases (3+)
- User Story 1 (US1) must complete before User Story 2 (branches, commit/diff)
- User Story 2 (branches, commit/diff) must complete before User Story 3 (content delivery)
- Final phase can run in parallel with last user story

---

## Parallel Execution Examples

- T001–T007 (setup) can run in parallel
- Within each user story, model, endpoint, test, and doc tasks can run in parallel if in different files
- BDD and unit tests can run in parallel with implementation if TDD is not required

---

## Implementation Strategy

- MVP: Complete User Story 1 (clone/list/switch repos) with full API, tests, and docs
- Incremental: Add branch management, commit/diff, then content delivery in order of priority
- Each user story is independently testable and deployable

---

# Summary

- Total tasks: 48
- User Story 1: 8 tasks
- User Story 2 (branches): 7 tasks
- User Story 2 (commit/diff): 7 tasks
- User Story 3: 8 tasks
- Parallel opportunities: setup, per-story (models, endpoints, tests, docs)
- Each story has independent test criteria
- MVP scope: User Story 1 (T013–T020)
