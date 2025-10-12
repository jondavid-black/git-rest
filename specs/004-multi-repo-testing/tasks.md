# Tasks: Multi-Repo Testing

## Phase 1: Setup Tasks

- **T001**: Ensure Python 3.12+ and all dependencies (Flask, gitpython, pydantic, pytest, Behave, uv, ruff) are installed. [P]
- **T002**: Verify test repos are accessible: https://github.com/jondavid-black/git-rest-test and https://github.com/jondavid-black/git-rest-test-other. [P]
- **T003**: Confirm filesystem-based per-user repo storage is configured. [P]
- **T004**: Prepare Behave BDD test environment in `tests/bdd/`.

## Phase 2: Foundational Tasks

- **T005**: Implement or verify user context/session management for active repo switching.
- **T006**: Ensure error handling for repo name collisions and invalid operations is in place.

## Phase 3: User Story 1 - Clone Multiple Repositories (P1)

- **US1 Goal**: User can clone both provided repositories and see them as independent entities.
- **Independent Test**: Clone both repos, list, and verify both are present and independent.
- **T007**: [P] Add BDD scenario: clone `git-rest-test` via API (tests/bdd/).
- **T008**: [P] Add BDD scenario: clone `git-rest-test-other` via API (tests/bdd/).
- **T009**: [P] Add BDD scenario: list all repos and verify both are present (tests/bdd/).
- **T010**: [P] Implement `/repos/clone` endpoint (src/git_rest/api/).
- **T011**: [P] Implement `/repos` list endpoint (src/git_rest/api/).
- **T012**: [P] Implement repo model logic for independent storage (src/git_rest/models/).
- **T013**: [P] Implement repo service logic for cloning and listing (src/git_rest/services/).
- **T014**: Integrate and validate all US1 tests pass.

## Phase 4: User Story 2 - Switch Between Managed Repositories (P2)

- **US2 Goal**: User can switch active context between managed repos.
- **Independent Test**: Switch context and verify subsequent actions apply only to selected repo.
- **T015**: [P] Add BDD scenario: switch context to `git-rest-test` (tests/bdd/).
- **T016**: [P] Add BDD scenario: switch context to `git-rest-test-other` (tests/bdd/).
- **T017**: [P] Implement `/repos/switch` endpoint (src/git_rest/api/).
- **T018**: [P] Implement context/session logic for switching (src/git_rest/services/).
- **T019**: Integrate and validate all US2 tests pass.

## Phase 5: User Story 3 - Isolated Commits and Repository State (P3)

- **US3 Goal**: Commits to one repo do not affect the other.
- **Independent Test**: Commit to one repo, verify no changes in the other.
- **T020**: [P] Add BDD scenario: commit to `git-rest-test` and verify isolation (tests/bdd/).
- **T021**: [P] Add BDD scenario: commit to `git-rest-test-other` and verify isolation (tests/bdd/).
- **T022**: [P] Implement `/repos/{name}/commit` endpoint (src/git_rest/api/).
- **T023**: [P] Implement commit logic with repo isolation (src/git_rest/services/).
- **T024**: Integrate and validate all US3 tests pass.

## Phase 6: User Story 4 - Repository Origin Integrity (P4)

- **US4 Goal**: The origin of each repo is correctly maintained and can be queried.
- **Independent Test**: Query origin for each repo and verify correct URL.
- **T025**: [P] Add BDD scenario: query origin for `git-rest-test` (tests/bdd/).
- **T026**: [P] Add BDD scenario: query origin for `git-rest-test-other` (tests/bdd/).
- **T027**: [P] Implement `/repos/{name}/origin` endpoint (src/git_rest/api/).
- **T028**: [P] Implement origin query logic (src/git_rest/services/).
- **T029**: Integrate and validate all US4 tests pass.

## Phase 7: Polish & Cross-Cutting Concerns

- **T030**: Add/verify edge case BDD scenarios: name collision, switching to non-existent repo, commit in detached HEAD (with measurable error outcome), network failure (tests/bdd/).
- **T033**: Add BDD scenario and/or monitoring to measure repo switch performance (<2s in 95% of cases) (tests/bdd/ or monitoring script).
- **T031**: Review and update documentation (quickstart.md, API docs, user flows).
- **T032**: Final CI/CD check: lint, format, test coverage, all tests passing.

## Dependencies
- US1 → US2, US3, US4 (US1 must be complete before others)
- US2, US3, US4 can proceed in parallel after US1

## Parallel Execution Examples
- T007, T008, T009, T010, T011, T012, T013 can be done in parallel (US1)
- T015, T016, T017, T018 can be done in parallel (US2)
- T020, T021, T022, T023 can be done in parallel (US3)
- T025, T026, T027, T028 can be done in parallel (US4)

## Implementation Strategy
- MVP: Complete all tasks for US1 (cloning and listing repos)
- Incremental: Add US2 (switching), US3 (commit isolation), US4 (origin integrity) in parallel after US1
- Polish: Edge cases, docs, CI/CD
