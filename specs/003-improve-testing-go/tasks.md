# Tasks: Improve Testing

## Phase 1: Setup

- **T001**: [P] Ensure Python 3.12+ and all dependencies (pytest, behave, ruff, uv, coverage) are installed (`requirements.txt`, `uv pip install -r requirements.txt`)
- **T002**: [P] Verify project structure matches plan (src/git_rest/, tests/unit/, tests/bdd/)
- **T003**: [P] Set up CI to run pytest, behave, and coverage checks on PRs

## Phase 2: Foundational Tasks

- **T004**: [P] Audit all Python files in src/git_rest/ for functions needing unit tests
- **T005**: [P] Generate initial coverage report (pytest --cov=src/git_rest)
- **T006**: [P] Identify all user workflows for BDD coverage (clone, branch, commit, pull, merge, push, multi-repo, multi-branch)

## Phase 3: User Story 1 - Unit Test Coverage for All Functions (P1)

- **T007**: [US1] For each function in src/git_rest/, write at least one nominal unit test (tests/unit/)
- **T008**: [US1] For functions with failure/off-nominal modes, write additional unit tests for error handling (tests/unit/)
- **T009**: [US1] Use mocks to isolate dependencies in unit tests (pytest-mock or unittest.mock)
- **T010**: [US1] Ensure all new/updated unit tests are repeatable and isolated
- **T011**: [US1] Re-run coverage and confirm at least 75% coverage
- **T012**: [US1] Document uncovered functions and create follow-up tasks if needed
- **T013**: [US1] Add/Update test documentation in quickstart.md
- **T014**: [US1] Checkpoint: All functions have at least one unit test and coverage >= 75%

## Phase 4: User Story 2 - BDD Workflow Coverage (P2)

- **T015**: [US2] Review and update BDD feature files in tests/bdd/ for all major workflows
- **T016**: [US2] Implement missing BDD step definitions for workflows (tests/bdd/steps/)
- **T017**: [US2] Emulate PR merge in BDD tests (no real remote)
- **T018**: [US2] Add BDD scenarios for multi-repo and multi-branch switching
- **T019**: [US2] Run behave and ensure all scenarios pass
- **T020**: [US2] Checkpoint: All major workflows covered by BDD and pass

## Phase 5: User Story 3 - Multi-Repo and Multi-Branch Support (P3)

- **T021**: [US3] Add/Update unit and BDD tests for cloning multiple repos and switching between them
- **T022**: [US3] Add/Update unit and BDD tests for creating/switching multiple branches per repo
- **T023**: [US3] Ensure correct context is maintained when switching repos/branches
- **T024**: [US3] Checkpoint: Multi-repo and multi-branch support tested and passing

## Phase 6: Polish & Cross-Cutting Concerns

- **T025**: [P] Review for duplicate/overlapping tests and consolidate
- **T026**: [P] Final code and test linting (ruff check .)
- **T027**: [P] Update documentation (README.md, quickstart.md) with test and coverage instructions
- **T028**: [P] Final checkpoint: All requirements and user stories independently testable

## Dependencies

- Phase 1 and 2 tasks can be done in parallel
- User Story phases (3, 4, 5) are sequential by priority (P1 → P2 → P3)
- Polish phase can begin after all user stories are complete

## Parallel Execution Examples

- T001, T002, T003 can run in parallel
- T004, T005, T006 can run in parallel
- Within each user story, test writing and implementation tasks can be parallelized by file

## Implementation Strategy

- MVP: Complete all tasks for User Story 1 (T007–T014)
- Incremental: Add BDD and multi-repo/branch support in subsequent phases

---

**Total tasks:** 28
**User Story 1 tasks:** 8
**User Story 2 tasks:** 6
**User Story 3 tasks:** 4
**Parallel opportunities:** 6 (setup, foundational, polish)
**Independent test criteria:** Each user story phase has a checkpoint task
**Suggested MVP:** Complete all User Story 1 tasks (unit test coverage)
