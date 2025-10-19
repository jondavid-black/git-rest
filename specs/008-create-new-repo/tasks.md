
# Tasks: Create New Repo

## Phase 1: Setup Tasks
T001: [P] Initialize project structure for new feature in `src/git_rest/` and `tests/` directories
T002: [P] Add/verify dependencies: Flask, GitPython, Pydantic, pytest, Behave, ruff in project config
T003: [P] Add/verify documentation structure in `specs/008-create-new-repo/`
T004: [P] Add project-level performance monitoring and logging setup (to support API response time and memory usage tracking)

## Phase 2: Foundational Tasks
T005: Implement base Repository, User, File, and Branch models in `src/git_rest/models/`
T006: Implement file-based storage utilities for per-user repo directories in `src/git_rest/utils/`
T007: Implement license text loader/validator in `src/git_rest/utils/`
T008: Add foundational error handling utilities and document error handling acceptance criteria

## Phase 3: User Story 1 - Create a New Repository (P1)
T009: Implement API endpoint `/api/repos` (POST) in `src/git_rest/api/` for repo creation
T010: Implement service logic for repo creation (validate input, create directory, add README.md, LICENSE) in `src/git_rest/services/`
T011: Integrate license validation and README.md handling in service logic
T012: [P] Add unit tests for repo creation (valid/invalid input, duplicate name, license errors, empty/large README) in `tests/unit/`
T013: [P] Add contract test (OpenAPI conformance) for `/api/repos` endpoint in `tests/contract/`
T014: [P] Add integration test for end-to-end repo creation in `tests/integration/`
T015: [P] Add Behave/BDD acceptance test for repo creation in `tests/contract/` (end-to-end, user-focused)
T016: Add validation test for measurable success criteria (repo creation <30s, correct files, error messages)
T017: Add validation test for API response time (<200ms p95) and memory usage (<100MB/process)
T018: Update documentation and quickstart for repo creation usage, including test type glossary
T019: Checkpoint: User Story 1 independently testable (repo can be created via API, with README and license, meets non-functional criteria)

## Phase 4: User Story 2 - Perform Git Operations on New Repo (P2)
T020: Implement file upload API for new repos in `src/git_rest/api/`
T021: Implement branch creation API for new repos in `src/git_rest/api/`
T022: Integrate with existing git-rest operations for new repos in `src/git_rest/services/`
T023: [P] Add unit tests for file upload and branch creation in `tests/unit/`
T024: [P] Add contract tests for file upload and branch creation endpoints in `tests/contract/`
T025: [P] Add integration tests for file upload and branch creation in `tests/integration/`
T026: [P] Add Behave/BDD acceptance test for file upload and branch creation in `tests/contract/`
T027: Add validation test for measurable success criteria (follow-up git operations without errors)
T028: Update documentation for new repo operations
T029: Checkpoint: User Story 2 independently testable (files and branches can be added to new repos, meets non-functional criteria)

## Final Phase: Polish & Cross-Cutting Concerns
T030: Review and improve error handling for all repo creation and git operations, ensuring all acceptance criteria are met
T031: Review and update API documentation (OpenAPI contract)
T032: Final code review, refactor, and ensure all tests/documentation are up to date

## Dependencies
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Final Phase
T005–T008 must complete before T009–T019
T009–T019 must complete before T020–T029

## Parallel Execution Examples
T001, T002, T003, T004 can be done in parallel
T012, T013, T014, T015 can be done in parallel after T011
T023, T024, T025, T026 can be done in parallel after T022

## Implementation Strategy
MVP: Complete all tasks through Phase 3 (User Story 1)
Incremental delivery: Each user story phase is independently testable and can be delivered/reviewed separately

## Task Count
Total: 32
User Story 1: 11 (T009–T019)
User Story 2: 10 (T020–T029)
Parallel opportunities: 12 ([P] tasks)
Each user story has clear independent test criteria and non-functional coverage
Suggested MVP scope: Complete through User Story 1 (T019)
