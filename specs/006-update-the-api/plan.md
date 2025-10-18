
# Implementation Plan: Update the API to allow a user to POST file content

**Branch**: `006-update-the-api` | **Date**: 2025-10-18 | **Spec**: specs/006-update-the-api/spec.md
**Input**: Feature specification from `specs/006-update-the-api/spec.md`

## Summary

Enable users to POST file content to update or create files in their own repositories, with user separation enforced in all endpoints. Implement a new POST endpoint at `/users/<user_id>/repos/<repo_id>/files/{file_path}` for file updates, respecting user isolation. The endpoint does not exist yet and must be added to the Flask blueprint in `src/git_rest/api/files.py`. All file and commit operations must use user-based URL structures as in the current system.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: Flask, gitpython, pydantic
**Storage**: Filesystem (git repo)
**Testing**: pytest, Behave
**Target Platform**: Linux server
**Project Type**: Single (backend REST API)
**Performance Goals**: <2s for file POST <1MB
**Constraints**: <100MB per file, sequential file-level update locking
**Scale/Scope**: Multiple users, multiple repos, file-level concurrency

## Constitution Check

All gates pass: Spec-driven development, system engineering baseline, test-first, automation, documentation, and technology stack are aligned with the constitution.

## Functional Requirements

- System MUST allow users to POST file content to update or create files in a repository.
- System MUST recognize file types (text, binary) and handle encoding/decoding as needed.
- System MUST stage file changes (similar to 'git add') but MUST NOT commit them until a separate commit API call is made.
- System MUST return a status code indicating success or error for each POST operation.
- System MUST support partial file updates (e.g., by line range or diff) to enhance performance.
- System MUST respect the current git branch and repository state when updating files.
- System MUST provide clear error messages for invalid operations (e.g., invalid file, branch, or content).
- System MUST allow retrieval of updated file content after a POST operation.
- System MUST handle concurrent updates and file locks gracefully by forcing updates to be sequential at the individual file level. If two users attempt to update the same file simultaneously, the system will process one update first and block the second until the first completes, minimizing blocking time for the second.

## User Scenarios & Testing

**P1:** Upload or update file content (text or binary) via API, verify content, ensure staged not committed.
**P2:** Partial file update (lines x-y), verify only specified lines change.
**P3:** Error handling for invalid file, branch, or content.

## Measurable Outcomes

- Users can update or create files via API POST in under 2 seconds for files <1MB.
- 100% of valid file POST operations result in the file being updated and staged, not committed.
- 95% of partial updates complete successfully and only affect the specified range.
- 100% of error cases return clear, actionable error messages and appropriate status codes.
- User acceptance test (clone repo, update README.md, POST, verify content) passes without manual intervention.

## Project Structure

### Documentation (this feature)

```
specs/006-update-the-api/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```
src/
├── git_rest/
│   ├── api/
│   │   ├── files.py  # user-based file endpoints
│   │   └── commit.py # user-based commit endpoint
│   └── ...
└── ...


├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Use user-based endpoints in `src/git_rest/api/files.py` and `src/git_rest/api/commit.py` as in the current system. Add new POST endpoint for file content under `/users/<user_id>/repos/<repo_id>/files/{file_path}`.

## Complexity Tracking

No constitution violations or rejected alternatives. All design choices align with project standards and constitution.
