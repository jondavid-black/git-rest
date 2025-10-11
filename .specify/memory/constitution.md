
# git-rest Constitution


## Core Principles

### I. Spec-Driven Development
All features and changes must begin with a written specification using the Spec-Kit approach. Specifications must be reviewed and approved before implementation begins. This ensures clarity, alignment, and testability from the outset.

### II. System Engineering Baseline
The project must maintain a solid system engineering baseline, including architecture, requirements, and acceptance criteria. All changes must be traceable to approved specs and baseline documents.

### III. Test-First (Unit & Acceptance)
Unit tests (pytest) and acceptance tests (Behave BDD) must be written before implementation. No code is merged without passing tests and meeting coverage requirements. Red-Green-Refactor is enforced.

### IV. Automation & CI/CD
All builds, tests, and deployments are automated using GitHub Actions. Python environments are managed with uv. Linting and formatting are enforced with ruff. No manual steps in the critical path.

### V. Documentation & Transparency
Documentation is mandatory and must be kept up to date. Mkdocs with the Material theme is used for the documentation site, which must include a splash screen, getting started, how-to, and API documentation. All design and process decisions are documented for transparency.


## Technology Stack & Tooling

- Python 3.12+ with Flask for REST API server
- Git as the SCM backend
- Spec-Kit for specification-driven development
- pytest for unit testing
- Behave for BDD acceptance testing
- uv for Python environment management
- ruff for linting and formatting
- GitHub Actions for CI/CD
- Mkdocs + Material theme for documentation
- MIT License


## Development Workflow

1. All work is performed in small, reviewable batches.
2. Each batch starts with a spec and plan, reviewed and approved before implementation.
3. Code is developed test-first, with both unit and acceptance tests.
4. Linting, formatting, and coverage checks are enforced in CI.
5. Documentation is updated with every change.
6. Only passing, reviewed, and documented changes are merged to main.


## Governance

This constitution supersedes all other practices for the git-rest project. Amendments require a documented proposal, review, and approval by project maintainers. All changes must be versioned according to semantic versioning:

- MAJOR: Backward-incompatible changes to principles or governance
- MINOR: New principles or sections, or major expansions
- PATCH: Clarifications, wording, or non-semantic refinements

Compliance is reviewed in every PR. All contributors must follow the constitution and reference the latest version in all planning and review processes. Runtime guidance is provided in the README and docs.

<!--
Sync Impact Report
Version change: none → 1.0.0
List of modified principles: N/A (initial version)
Added sections: All
Removed sections: None
Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
Follow-up TODOs: None
-->

**Version**: 1.0.0 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-11