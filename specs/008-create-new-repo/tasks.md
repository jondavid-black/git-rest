

# Tasks: Create & Clone Repo

## Section 1: Create New Repository (MVP)
1. Implement API endpoint `POST /api/repos/create` for repo creation
2. Implement service logic: validate input, create directory, add README.md and LICENSE if provided
3. Validate required fields and reject duplicate repo names per user
4. Handle license validation and error cases
5. Add unit tests for create (valid/invalid input, duplicate name, license errors, empty/large README)
6. Add BDD/acceptance test for create (end-to-end)
7. Update documentation and quickstart for create usage
8. Checkpoint: Create independently testable (repo can be created via API, with README and license, meets non-functional criteria)

## Section 2: Clone Remote Repository
9. Implement API endpoint `POST /api/repos/clone` for repo cloning
10. Implement service logic: validate input, perform git clone, handle new name/description if provided
11. Validate required fields and reject duplicate repo names per user
12. Handle invalid/unreachable remote errors
13. Add unit tests for clone (valid/invalid input, duplicate name, remote errors)
14. Add BDD/acceptance test for clone (end-to-end)
15. Update documentation and quickstart for clone usage
16. Checkpoint: Clone independently testable (repo can be cloned via API, meets non-functional criteria)

## Section 3: Git Operations on New/Cloned Repo
17. Implement file upload API for new/cloned repos
18. Implement branch creation API for new/cloned repos
19. Add unit and BDD tests for file upload and branch creation
20. Update documentation for new repo operations
21. Checkpoint: Git operations independently testable (files and branches can be added, meets non-functional criteria)

## Implementation Strategy
- MVP: Complete all tasks in Section 1 (Create New Repository)
- Section 2 (Clone) and Section 3 (Git Operations) can be delivered incrementally

## Notes
- Each user story is independently testable and has clear acceptance criteria
- Defer non-essential setup, performance, and cross-cutting tasks until after MVP
Each user story has clear independent test criteria and non-functional coverage
Suggested MVP scope: Complete through User Story 1 (T019)
