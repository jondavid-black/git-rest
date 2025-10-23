# Tasks: Explicit Clone URL API Endpoint

## Phase 1: Setup
- T001: [P] Ensure Python 3.12+ environment is active
- T002: [P] Confirm Flask, gitpython, pydantic are installed
- T003: [P] Validate filesystem structure for per-user repo directories

## Phase 2: Foundational
- T004: [P] Review and update error handling conventions in repo service
- T005: [P] Confirm user namespace logic is robust

## Phase 3: User Story 1 (P1) - Clone Repository via Explicit Endpoint
- T006: [P] Update `src/git_rest/api/repos.py` to add POST `/api/<user_id>/repos/clone` endpoint
- T007: [P] Implement clone logic using gitpython for the new endpoint
- T008: [P] Validate clone URL and handle errors (invalid, unreachable)
- T009: [P] Add/Update unit tests for clone endpoint in `tests/unit/`
- T010: [P] Add/Update BDD tests for clone endpoint in `tests/bdd/`
- T011: [P] Document new endpoint in API docs
- T012: [P] Check for duplicate repo names and handle accordingly
- T013: [P] Handle permission errors for cloning
- T014: [P] Integration test: POST to new endpoint and verify repo is cloned
- T015: [P] Remove clone logic from old endpoint in `src/git_rest/api/repos.py`
- T016: [P] Remove/Update tests referencing old endpoint

## Phase 4: User Story 2 (P2) - Remove Ambiguity in Repo Creation
- T017: [P] Ensure repo creation and clone endpoints are distinct in code and docs
- T018: [P] Test that POST to old endpoint does not clone
- T019: [P] Update documentation to clarify endpoint separation

## Phase 5: User Story 3 (P3) - Documentation and Test Coverage
- T020: [P] Review all documentation for endpoint accuracy
- T021: [P] Ensure all tests reference new endpoint and pass
- T022: [P] Final review for maintainability and reliability


## Phase 6: Polish & Cross-Cutting Concerns
- T023: [P] Final code linting and formatting (ruff)
- T024: [P] Final CI/CD pipeline check (GitHub Actions)
- T025: [P] Update Mkdocs site with new API details
- T026: [P] Performance validation: Test clone endpoint latency (<500ms typical)
- T027: [P] Security validation: Confirm endpoint access controls and error handling

## Dependencies
- User Story 1 must complete before User Story 2 and 3
- Setup and Foundational phases must complete before any user story

## Parallel Execution Examples
- All tasks within each phase marked [P] can be executed in parallel
- Example: T006–T016 can be worked on by multiple contributors simultaneously

## Implementation Strategy
- MVP: Complete all tasks for User Story 1 (Phase 3)
- Incremental delivery: Complete subsequent phases after MVP
