# Research: Multi-Repo Testing

## Decision: Use Behave BDD for Multi-Repo Scenarios
- **Rationale**: Behave is already used for acceptance testing in git-rest. It supports scenario-driven, user-focused tests and integrates with the current Python/Flask stack. BDD is ideal for validating user flows like multi-repo management.
- **Alternatives considered**: Manual API tests (less maintainable), custom scripts (less readable), other BDD tools (Behave is already standard).

## Decision: Filesystem-based Repo Isolation
- **Rationale**: The current architecture uses per-user directories for repo storage, which naturally isolates repositories. This matches the requirement for commit and state isolation.
- **Alternatives considered**: Database-backed repo tracking (unnecessary complexity for current scope), in-memory (not persistent).

## Decision: Test Repos are Public
- **Rationale**: The provided test repos are public, so no authentication is needed for cloning. This simplifies test setup and avoids secrets management.
- **Alternatives considered**: Private repos (would require auth setup).

## Decision: Error Handling for Name Collisions
- **Rationale**: The spec requires clear error messages for repo name collisions. The system will reject duplicate names and return actionable errors.
- **Alternatives considered**: Auto-renaming (could confuse users), silent overwrite (data loss risk).

## Decision: Performance Target for Switching
- **Rationale**: The spec sets a 2s target for switching repos. This is reasonable for local filesystem operations and ensures a responsive UX.
- **Alternatives considered**: Stricter targets (may not be needed for MVP), looser targets (worse UX).
