# Research: Create New Repo

## Decision: Python 3.12+ with Flask, GitPython, Pydantic, file-based storage
- **Rationale**: Aligns with project standards, supports REST API, and integrates with git operations. File-based storage matches current architecture and user isolation needs.
- **Alternatives considered**: FastAPI (not project standard), database-backed storage (unnecessary for current scale), custom git CLI wrappers (less maintainable).

## Decision: API endpoint design
- **Rationale**: RESTful POST endpoint for repo creation is standard and easily testable. Optional fields for README and license provide flexibility.
- **Alternatives considered**: GraphQL (overkill for simple CRUD), CLI-only interface (not user-friendly for web clients).

## Decision: License handling
- **Rationale**: Use official license texts for common open source licenses. Return error for unrecognized names to avoid legal ambiguity.
- **Alternatives considered**: Guessing license text (risk of error), allowing custom license uploads (out of scope for MVP).

## Decision: Repo name uniqueness per user
- **Rationale**: Allows users to have their own namespace, avoids global name conflicts, matches common git hosting patterns.
- **Alternatives considered**: Global uniqueness (restrictive, not user-friendly), case-insensitive matching (could cause confusion).
