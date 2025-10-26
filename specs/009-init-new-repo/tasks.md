# Tasks for Init New Repo API Endpoint

## Phase 1: Setup Tasks

- T001: Ensure Python 3.12+ environment with Flask, gitpython, pydantic, pytest, Behave, and ruff installed [P]
- T002: Confirm filesystem structure for per-user repo directories exists [P]
- T003: Verify test and documentation infrastructure (pytest, Behave, Mkdocs) [P]

## Phase 2: Foundational Tasks

- T004: Define or update `User` and `Repository` models in `src/git_rest/models/` [P]
- T005: Implement or update repository service logic for repo creation in `src/git_rest/services/` [P]

## Phase 3: User Story 1 - Create New Repository (P1)

- T006: Write unit tests for repo creation logic in `tests/unit/test_api_repos.py`
- T007: Implement `/users/<user_id>/repos/init` POST endpoint in `src/git_rest/api/repos.py`
- T008: Integrate repo name validation (letters, numbers, dashes, underscores) [P]
- T009: Ensure endpoint returns correct URL on success [P]
- T010: Handle errors: duplicate repo, invalid name, missing user, storage failure [P]
- T011: Write BDD scenario for repo creation in `tests/bdd/repos.feature`
- T012: Update or create supporting step definitions for BDD in `tests/bdd/steps/`
- T013: Update or create documentation for endpoint in `docs/api.md`, `docs/getting-started.md`, `docs/how-to.md` [P]
- T014: Manual/automated test: POST to endpoint, verify repo is created and URL returned
- T015: Checkpoint: All tests for repo creation pass independently

## Phase 4: User Story 2 - Backward Compatibility (P2)

- T016: Run regression tests for all existing `/users/<user>/repos/<repo>` endpoints
- T017: Verify no regressions in repo/branch commands for new and existing repos
- T018: Checkpoint: All existing endpoints function as before

## Phase 5: User Story 3 - Documentation and Discoverability (P3)

- T019: Review and update documentation for clarity and completeness in `docs/api.md`, `docs/getting-started.md`, `docs/how-to.md`
- T020: Check documentation for discoverability of new endpoint
- T021: Checkpoint: Documentation reviewed and approved

## Final Phase: Polish & Cross-Cutting Concerns

- T022: Code review and refactor for maintainability
- T023: Final integration test: end-to-end repo creation and usage
- T024: Ensure all tests (unit, BDD, regression) pass in CI
- T025: Final documentation polish and Mkdocs build

## Dependencies

- Phase 1 tasks can be done in parallel
- Phase 2 tasks can be done in parallel after setup
- Phase 3 (US1) depends on foundational tasks
- Phase 4 (US2) depends on US1 completion
- Phase 5 (US3) can be done in parallel with Phase 4
- Final phase depends on all previous phases

## Parallel Execution Examples

- T001, T002, T003 [P]
- T004, T005 [P]
- T008, T009, T010, T013 [P] (after T007)

## Implementation Strategy

- MVP: Complete all tasks for User Story 1 (T006–T015)
- Incremental delivery: Each user story phase is independently testable and can be merged after checkpoint

---

**Total tasks:** 25
- User Story 1: 10
- User Story 2: 3
- User Story 3: 3
- Setup/Foundational/Polish: 9
- Parallel opportunities: 9 tasks marked [P]
- Each user story has independent test criteria and checkpoint
- Suggested MVP: Complete User Story 1 (repo creation endpoint, tests, docs)
