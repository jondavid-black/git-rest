# Tasks: Update the API to allow a user to POST file content

## Phase 1: Setup Tasks
- T001: [P] Ensure Python 3.12+ environment is available
- T002: [P] Install Flask, gitpython, pydantic, pytest, Behave
- T003: [P] Initialize or verify repository structure for user separation
- T004: [P] Document API endpoints and usage in quickstart.md


## Phase 2: Foundational Tasks
T005: Implement base models for File, Repository, User in `src/git_rest/models/`
T006: Implement file locking and sequential update logic in service layer (define measurable criteria for sequential: e.g., max wait time, queueing, error on timeout)
T007: Implement validation utilities for file type, encoding, and branch state
T007a: Implement and test binary file encoding/decoding logic in service layer
T007b: Implement and test performance metrics collection for file POST (<2s server response for <1MB)
T007c: Implement and test scalability limits (file size, concurrent users)


## Phase 3: User Story 1 (P1) - Upload or Update File Content
T008: [Story US1] Design POST endpoint in OpenAPI contract for `/users/{user_id}/repos/{repo_id}/files/{file_path}`
T009: [Story US1] Implement POST endpoint in `src/git_rest/api/files.py` to update or create file content (text/binary)
T010: [Story US1] Add staging logic (do not commit on POST)
T011: [Story US1] Implement retrieval logic for updated file content (GET)
T012: [Story US1] [P] Write unit tests for POST, GET, and binary file handling endpoints (pytest)
T013: [Story US1] [P] Write acceptance test for full workflow (Behave): clone repo, GET README.md, POST update, GET README.md, verify content
T014: [Story US1] [P] Document endpoint usage in quickstart.md
T015: [Story US1] [P] Update contracts/openapi.yaml with endpoint details
T016: [Story US1] [P] Update data-model.md with any new attributes
T017: [Story US1] [P] Update research.md with implementation decisions
T018: [Story US1] [P] Update plan.md with implementation notes
T018a: [Story US1] [P] Write unit and acceptance tests for performance and scalability (pytest, Behave)


## Phase 4: User Story 2 (P2) - Partial File Update
T019: [Story US2] Design partial update payload (line range/diff) in OpenAPI contract
T020: [Story US2] Implement partial update logic in POST endpoint (support both line range and diff)
T021: [Story US2] [P] Write unit tests for partial update logic (line range and diff)
T022: [Story US2] [P] Write acceptance test for partial update workflow
T023: [Story US2] [P] Document partial update usage in quickstart.md
T024: [Story US2] [P] Update contracts/openapi.yaml with partial update details
T025: [Story US2] [P] Update data-model.md with any new attributes
T026: [Story US2] [P] Update research.md with implementation decisions
T027: [Story US2] [P] Update plan.md with implementation notes


## Phase 5: User Story 3 (P3) - Error Handling and Status Codes
T028: [Story US3] Implement error handling for invalid file path, branch, or content in POST endpoint
T029: [Story US3] Implement error handling for concurrent update (409), including explicit rollback/recovery logic for simultaneous updates
T030: [Story US3] [P] Write unit tests for error cases (consolidate duplicate error test tasks)
T031: [Story US3] [P] Write acceptance test for error scenarios
T032: [Story US3] [P] Document error handling in quickstart.md
T033: [Story US3] [P] Update contracts/openapi.yaml with error codes
T034: [Story US3] [P] Update data-model.md with any new attributes
T035: [Story US3] [P] Update research.md with error handling decisions
T036: [Story US3] [P] Update plan.md with implementation notes

## Phase 6: Polish & Cross-Cutting Concerns
- T037: [P] Refactor code for maintainability and clarity
- T038: [P] Ensure all documentation is up to date
- T039: [P] Final review and code cleanup


## Dependencies
Setup and foundational tasks must complete before any user story phase
User Story 1 (US1) is MVP and can be delivered independently
User Story 2 (US2) depends on US1
User Story 3 (US3) depends on US1 and US2
Polish phase can run after all user stories
All terminology for user must be normalized to "user_id" across all code, docs, and tests

## Parallel Execution Examples
- T001-T004 can run in parallel
- Within each user story, tasks marked [P] can run in parallel (e.g., tests, docs, contract updates)

## Implementation Strategy
- Deliver MVP with User Story 1 (US1): POST/GET endpoints, staging logic, tests, docs
- Incrementally add partial update (US2) and error handling (US3)
- Refactor and polish after all stories are complete

## Task Count
- Total tasks: 39
- US1: 11 tasks (T008-T018)
- US2: 9 tasks (T019-T027)
- US3: 9 tasks (T028-T036)
- Setup/Foundational/Polish: 10 tasks
- Parallel opportunities: 22 tasks
- Each user story is independently testable
- Suggested MVP scope: User Story 1 (US1)
