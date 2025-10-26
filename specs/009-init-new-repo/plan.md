
# Implementation Plan: Init New Repo API Endpoint

**Branch**: `009-init-new-repo` | **Date**: 2025-10-26 | **Spec**: specs/009-init-new-repo/spec.md
**Input**: Feature specification from `/specs/009-init-new-repo/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add a new API endpoint at `/users/<user_id>/repos/init` (POST) to allow users to create and initialize a new git repository by providing a repo name. The endpoint returns the URL to the new repository. The system must handle concurrent repo creation requests safely, return measurable error messages for storage failures, and provide a measurable performance metric for repo creation (<5s). All existing repo APIs remain unchanged. Unit and BDD tests, as well as documentation updates, are required.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: Flask, gitpython, pydantic
**Storage**: Filesystem (per-user repo directories)
**Testing**: pytest, Behave
**Target Platform**: Linux server
**Project Type**: single (monorepo, src/)
**Performance Goals**: Repo creation in <5s, 100% correct URL return
**Constraints**: No regressions in existing endpoints, repo names unique per user, standard git naming
**Scale/Scope**: 1000s of users, 1000s of repos per user

## Constitution Check

All gates pass:
- Spec-driven development: Spec is present and approved
- System engineering baseline: Requirements and acceptance criteria are clear
- Test-first: Unit and BDD tests required before implementation
- Automation & CI/CD: All builds/tests automated, Python env managed with uv, ruff for linting
- Documentation: Updates to api.md, getting-started.md, how-to.md required


## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
# Single project (DEFAULT)
src/
└── git_rest/
        ├── api/
        ├── models/
        └── services/

tests/
├── bdd/
└── unit/
```
**Structure Decision**: Preserve existing project structure.
